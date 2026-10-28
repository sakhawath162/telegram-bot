#!/usr/bin/env python3
"""Good Morning Bot: helps you send sweet good-morning texts to your partner.

Zero dependencies, standard library only. Run with: python3 bot.py
"""
import json
import logging
import os
import random
import secrets
import sqlite3
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from messages import MESSAGES, PET_NAMES

BASE_DIR = Path(__file__).resolve().parent


def load_env(path):
    """Minimal .env reader so we don't need python-dotenv."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env(BASE_DIR / ".env")
TOKEN = os.environ.get("BOT_TOKEN", "")
DEFAULT_TZ = os.environ.get("DEFAULT_TZ", "Asia/Dhaka")
DB_PATH = os.environ.get("DB_PATH", str(BASE_DIR / "bot.db"))
API_URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("bot")

STYLES = {
    "cute": "🧸 Cute",
    "romantic": "❤️ Romantic",
    "funny": "😂 Funny",
    "poetic": "🌅 Poetic",
    "mix": "🎲 Surprise me",
}

COMMANDS_MENU = [
    ("morning", "Get a sweet good-morning text"),
    ("style", "Choose the vibe of your messages"),
    ("name", "Set your partner's nickname"),
    ("link", "Connect your partner"),
    ("schedule", "Auto-send every morning, e.g. /schedule 07:30"),
    ("unschedule", "Stop the daily auto-send"),
    ("timezone", "Set your timezone, e.g. /timezone Asia/Dhaka"),
    ("unlink", "Disconnect your partner"),
    ("help", "Show what I can do"),
]

HELP = """☀️ I help you send sweet good-morning texts to your love.

/morning: get a sweet message (copy it, forward it, or send it straight to your partner)
/style: cute, romantic, funny or poetic
/name Jaan: what to call your partner in the messages

💞 Send messages through me:
/link: get an invite link for your partner. Once they open it, you can send messages to them with one tap.
/schedule 07:30: I'll send them a good morning every day at that time
/unschedule: stop the daily message
/timezone Asia/Dhaka: set your timezone (default: {tz})
/unlink: disconnect"""

bot_username = ""
inline_enabled = False


# ---------- Telegram API ----------

class TelegramError(Exception):
    pass


def api(method, **params):
    req = urllib.request.Request(
        f"{API_URL}/{method}",
        data=json.dumps(params).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            result = json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            result = json.load(e)
        except ValueError:
            raise TelegramError(f"{method}: HTTP {e.code}") from e
    if not result.get("ok"):
        raise TelegramError(f"{method}: {result.get('description')}")
    return result["result"]


def send(chat_id, text, **kwargs):
    return api("sendMessage", chat_id=chat_id, text=text, **kwargs)


# ---------- Storage ----------

db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        chat_id    INTEGER PRIMARY KEY,
        first_name TEXT,
        nickname   TEXT,
        style      TEXT DEFAULT 'mix',
        partner_id INTEGER,
        link_code  TEXT,
        send_time  TEXT,
        tz         TEXT,
        last_sent  TEXT
    )""")
db.commit()


def get_user(chat_id, first_name=None):
    db.execute("INSERT OR IGNORE INTO users (chat_id, tz) VALUES (?, ?)", (chat_id, DEFAULT_TZ))
    if first_name:
        db.execute("UPDATE users SET first_name=? WHERE chat_id=?", (first_name, chat_id))
    db.commit()
    return find_user(chat_id)


def find_user(chat_id):
    return db.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,)).fetchone()


def update_user(chat_id, **fields):
    cols = ", ".join(f"{key}=?" for key in fields)
    db.execute(f"UPDATE users SET {cols} WHERE chat_id=?", (*fields.values(), chat_id))
    db.commit()


def user_tz(user):
    try:
        return ZoneInfo(user["tz"] or DEFAULT_TZ)
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def partner_label(user):
    if user["nickname"]:
        return user["nickname"]
    partner = find_user(user["partner_id"]) if user["partner_id"] else None
    return (partner and partner["first_name"]) or "your partner"


# ---------- Messages ----------

def templates(style):
    """Return (style, template) pairs for a style; 'mix' means all of them."""
    styles = [style] if style in MESSAGES else list(MESSAGES)
    return [(s, t) for s in styles for t in MESSAGES[s]]


def fill(template, name):
    return template.format(name=name or random.choice(PET_NAMES))


def sweet_message(user):
    _, template = random.choice(templates(user["style"]))
    return fill(template, user["nickname"])


def message_keyboard(user):
    rows = [[{"text": "🔄 Another one", "callback_data": "more"}]]
    if user["partner_id"]:
        rows[0].append({"text": f"💌 Send to {partner_label(user)}", "callback_data": "send"})
    if inline_enabled:
        rows.append([{"text": "📤 Pick one in any chat", "switch_inline_query": user["nickname"] or ""}])
    return {"inline_keyboard": rows}


def deliver(sender, text):
    """Send a message to the sender's partner. Returns True on success."""
    if not sender["partner_id"]:
        return False
    try:
        send(sender["partner_id"], f"💌 From {sender['first_name'] or 'your love'}:\n\n{text}")
        return True
    except TelegramError as e:
        log.warning("Could not deliver to %s: %s", sender["partner_id"], e)
        return False


# ---------- Commands ----------

def cmd_start(user, arg):
    if arg:
        return accept_invite(user, arg)
    send(user["chat_id"], f"Hi {user['first_name'] or 'there'}! 💕\n\n" + HELP.format(tz=DEFAULT_TZ))


def cmd_help(user, arg):
    send(user["chat_id"], HELP.format(tz=DEFAULT_TZ))


def cmd_morning(user, arg):
    send(user["chat_id"], sweet_message(user), reply_markup=message_keyboard(user))


def cmd_style(user, arg):
    buttons = [[{"text": ("✅ " if key == user["style"] else "") + label, "callback_data": f"style:{key}"}]
               for key, label in STYLES.items()]
    send(user["chat_id"], "Pick the vibe for your good-morning texts:", reply_markup={"inline_keyboard": buttons})


def cmd_name(user, arg):
    if not arg:
        current = user["nickname"] or "not set (I'll use sweet pet names)"
        return send(user["chat_id"], f"Nickname: {current}\n\nSet one with /name Jaan\nClear it with /name -")
    nickname = None if arg == "-" else arg[:32]
    update_user(user["chat_id"], nickname=nickname)
    send(user["chat_id"], f"Got it! I'll call them {nickname} 💕" if nickname else "Nickname cleared.")


def cmd_link(user, arg):
    if user["partner_id"]:
        return send(user["chat_id"], f"You're already linked with {partner_label(user)} 💞 Use /unlink to disconnect.")
    code = secrets.token_urlsafe(8)
    update_user(user["chat_id"], link_code=code)
    send(user["chat_id"],
         "Send this link to your partner 💌\n\n"
         f"https://t.me/{bot_username}?start={code}\n\n"
         "Once they open it and tap Start, you'll be connected and can send them messages through me.")


def accept_invite(user, code):
    inviter = db.execute("SELECT * FROM users WHERE link_code=?", (code,)).fetchone()
    if not inviter:
        return send(user["chat_id"], "This invite link is invalid or was already used. Ask for a new one 🙏")
    if inviter["chat_id"] == user["chat_id"]:
        return send(user["chat_id"], "That's your own invite link 😄 Send it to your partner instead.")
    # Drop any previous partnerships of either person before connecting them.
    db.execute("UPDATE users SET partner_id=NULL WHERE partner_id IN (?, ?)", (user["chat_id"], inviter["chat_id"]))
    update_user(user["chat_id"], partner_id=inviter["chat_id"])
    update_user(inviter["chat_id"], partner_id=user["chat_id"], link_code=None)
    send(user["chat_id"], f"You're now connected with {inviter['first_name'] or 'your partner'} 💞\n\n"
                          "Expect sweet mornings! You can send them some too with /morning.")
    send(inviter["chat_id"], f"{user['first_name'] or 'Your partner'} accepted your invite 💞\n\n"
                             "Try /morning, or /schedule 07:30 to send them a good morning every day.")


def cmd_unlink(user, arg):
    if not user["partner_id"]:
        return send(user["chat_id"], "You're not linked with anyone. Use /link to invite your partner.")
    partner_id = user["partner_id"]
    update_user(user["chat_id"], partner_id=None)
    partner = find_user(partner_id)
    if partner and partner["partner_id"] == user["chat_id"]:
        update_user(partner_id, partner_id=None)
        try:
            send(partner_id, f"{user['first_name'] or 'Your partner'} disconnected from you.")
        except TelegramError:
            pass
    send(user["chat_id"], "Disconnected.")


def cmd_schedule(user, arg):
    tz_name = user["tz"] or DEFAULT_TZ
    if not arg:
        current = f"every day at {user['send_time']} ({tz_name})" if user["send_time"] else "off"
        return send(user["chat_id"], f"Daily good morning: {current}\n\nSet it with /schedule 07:30")
    try:
        send_time = datetime.strptime(arg, "%H:%M").strftime("%H:%M")
    except ValueError:
        return send(user["chat_id"], "Please use 24-hour HH:MM format, e.g. /schedule 07:30")
    now = datetime.now(user_tz(user))
    # If that time has already passed today, start tomorrow.
    last_sent = now.date().isoformat() if now.strftime("%H:%M") >= send_time else None
    update_user(user["chat_id"], send_time=send_time, last_sent=last_sent)
    reply = f"⏰ Every day at {send_time} ({tz_name}) I'll send {partner_label(user)} a sweet good morning ☀️"
    if not user["partner_id"]:
        reply += "\n\nYou're not linked yet, so use /link to invite your partner first."
    send(user["chat_id"], reply + "\n\nWrong timezone? Use /timezone Area/City")


def cmd_unschedule(user, arg):
    update_user(user["chat_id"], send_time=None)
    send(user["chat_id"], "Daily good morning turned off.")


def cmd_timezone(user, arg):
    if not arg:
        return send(user["chat_id"], f"Your timezone: {user['tz'] or DEFAULT_TZ}\n\n"
                                     "Change it with e.g. /timezone Asia/Dhaka or /timezone Europe/London")
    try:
        ZoneInfo(arg)
    except (ZoneInfoNotFoundError, ValueError):
        return send(user["chat_id"], "I don't know that timezone. Try something like Asia/Dhaka, Asia/Kolkata, "
                                     "Europe/London or America/New_York.")
    update_user(user["chat_id"], tz=arg)
    send(user["chat_id"], f"Timezone set to {arg} 🌍")


COMMANDS = {
    "/start": cmd_start,
    "/help": cmd_help,
    "/morning": cmd_morning,
    "/style": cmd_style,
    "/name": cmd_name,
    "/link": cmd_link,
    "/unlink": cmd_unlink,
    "/schedule": cmd_schedule,
    "/unschedule": cmd_unschedule,
    "/timezone": cmd_timezone,
}


# ---------- Update handlers ----------

def handle_message(msg):
    if msg["chat"]["type"] != "private":
        return
    user = get_user(msg["chat"]["id"], msg["from"].get("first_name"))
    cmd, _, arg = (msg.get("text") or "").strip().partition(" ")
    handler = COMMANDS.get(cmd.split("@")[0].lower())
    if handler:
        handler(user, arg.strip())
    else:
        send(user["chat_id"], "Tap /morning for a sweet good-morning text 💌 or /help to see everything I can do.")


def handle_callback(query):
    notice = None
    try:
        msg = query.get("message")
        if not msg:
            return
        user = get_user(query["from"]["id"], query["from"].get("first_name"))
        chat_id, message_id, data = msg["chat"]["id"], msg["message_id"], query.get("data", "")

        if data == "more":
            api("editMessageText", chat_id=chat_id, message_id=message_id,
                text=sweet_message(user), reply_markup=message_keyboard(user))
        elif data == "send":
            if deliver(user, msg.get("text", "")):
                notice = f"Sent to {partner_label(user)} 💌"
                sent_markup = {"inline_keyboard": [[{"text": "✅ Sent! Get another one", "callback_data": "more"}]]}
                api("editMessageReplyMarkup", chat_id=chat_id, message_id=message_id, reply_markup=sent_markup)
            else:
                notice = "Couldn't send it. Are you still linked? Try /link"
        elif data.startswith("style:") and data[6:] in STYLES:
            update_user(user["chat_id"], style=data[6:])
            api("editMessageText", chat_id=chat_id, message_id=message_id,
                text=f"Style set to {STYLES[data[6:]]}. Tap /morning to try it!")
    finally:
        api("answerCallbackQuery", callback_query_id=query["id"], text=notice or "")


def handle_inline(query):
    """Inline mode: type @botname in any chat to pick a message. Optional query = nickname."""
    user = find_user(query["from"]["id"])
    name = query.get("query", "").strip()[:32] or (user and user["nickname"]) or random.choice(PET_NAMES)
    pool = templates(user["style"] if user else "mix")
    results = []
    for i, (style, template) in enumerate(random.sample(pool, min(10, len(pool)))):
        text = fill(template, name)
        results.append({
            "type": "article",
            "id": str(i),
            "title": f"{STYLES[style]} good morning",
            "description": text,
            "input_message_content": {"message_text": text},
        })
    api("answerInlineQuery", inline_query_id=query["id"], results=results, cache_time=0, is_personal=True)


def dispatch(update):
    if "message" in update:
        handle_message(update["message"])
    elif "callback_query" in update:
        handle_callback(update["callback_query"])
    elif "inline_query" in update:
        handle_inline(update["inline_query"])


# ---------- Daily scheduler ----------

def run_schedules():
    rows = db.execute("SELECT * FROM users WHERE send_time IS NOT NULL AND partner_id IS NOT NULL").fetchall()
    for user in rows:
        now = datetime.now(user_tz(user))
        today = now.date().isoformat()
        if user["last_sent"] == today:
            continue
        hour, minute = map(int, user["send_time"].split(":"))
        minutes_late = (now.hour * 60 + now.minute) - (hour * 60 + minute)
        # Only send within an hour of the chosen time, so a restart doesn't fire stale messages.
        if not 0 <= minutes_late < 60:
            continue
        update_user(user["chat_id"], last_sent=today)
        text = sweet_message(user)
        try:
            if deliver(user, text):
                send(user["chat_id"], f"☀️ Sent your good morning to {partner_label(user)}:\n\n{text}")
            else:
                send(user["chat_id"], "I couldn't deliver today's good morning 😢 "
                                      "Your partner may have blocked or stopped the bot.")
        except TelegramError as e:
            log.warning("Scheduler notify failed for %s: %s", user["chat_id"], e)


# ---------- Main loop ----------

def main():
    global bot_username, inline_enabled
    if not TOKEN:
        raise SystemExit("BOT_TOKEN is missing. Put it in .env (get one from @BotFather).")
    try:
        me = api("getMe")
    except TelegramError as e:
        raise SystemExit(f"Telegram rejected the token ({e}). Double-check BOT_TOKEN in .env.")
    bot_username = me["username"]
    inline_enabled = me.get("supports_inline_queries", False)
    api("setMyCommands", commands=[{"command": c, "description": d} for c, d in COMMANDS_MENU])
    log.info("Running as @%s (inline mode: %s)", bot_username, "on" if inline_enabled else "off")

    offset, last_check = 0, 0.0
    while True:
        try:
            updates = api("getUpdates", offset=offset, timeout=25,
                          allowed_updates=["message", "callback_query", "inline_query"])
        except (TelegramError, OSError) as e:
            log.warning("Polling failed: %s", e)
            updates = []
            time.sleep(5)
        for update in updates:
            offset = update["update_id"] + 1
            try:
                dispatch(update)
            except Exception:
                log.exception("Failed to handle update %s", update.get("update_id"))
        if time.monotonic() - last_check >= 30:
            last_check = time.monotonic()
            try:
                run_schedules()
            except Exception:
                log.exception("Scheduler failed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye 👋")
