# 😘 Kiss Me Awake

A tiny Telegram bot ([@ClaudebshsushbsBot](https://t.me/ClaudebshsushbsBot)) that writes sweet good-morning texts for your girlfriend or boyfriend, and can deliver them for you every morning.

It uses only the Python standard library, so there's nothing to `pip install`.

## Features

- `/morning` gives you a sweet message with a 🔄 *Another one* button
- `/style` lets you pick cute, romantic, funny, poetic, or a mix
- `/name Jaan` personalizes every message with your partner's nickname
- `/link` sends your partner an invite. Once they accept, a 💌 *Send to partner* button appears.
- `/schedule 07:30` sends your partner a good morning automatically every day
- Inline mode (optional): type `@yourbot` in **any** Telegram chat (for example, your chat with your partner) and tap a message to send it as yourself. Your partner doesn't even need to use the bot.

> Why is linking needed? Telegram bots can only message people who have started the bot. Inline mode works around that because the message is sent by *you*.

## Setup

1. **Create the bot**: open [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`, and copy the token.
2. **(Recommended) Turn on inline mode**: in BotFather, send `/setinline`, choose your bot, and set the placeholder to e.g. `partner's name…`.
3. **Configure**:
   ```bash
   cp .env.example .env
   # edit .env and paste your BOT_TOKEN
   ```
4. **Run**:
   ```bash
   python3 bot.py
   ```
   Ubuntu already ships Python 3.12, so this works as is. Stop it with `Ctrl+C`.

Data is stored in `bot.db` (SQLite) next to the script.

## Keep it running 24/7

The daily `/schedule` only works while the bot is running. Pick one:

**Docker** (about 50 MB image):
```bash
docker build -t goodmorning-bot .
docker run -d --name goodmorning-bot --restart unless-stopped \
  --env-file .env -v goodmorning-data:/data goodmorning-bot
```

**Background process on this machine**:
```bash
nohup python3 bot.py > bot.log 2>&1 &
```

## Customize messages

Edit [messages.py](messages.py) and add your own lines to any category. Use `{name}` where the nickname should go.
