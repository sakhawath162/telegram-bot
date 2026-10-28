"""Storylines for /nonstop: short message chains that continue from one text to the next.

Each story is a list of steps, and each step is a list of variants (one is picked at random).
`{name}` is replaced with your partner's nickname.
"""
import random

# (start hour, phase). The last phase wraps around midnight.
PHASES = [(5, "morning"), (11, "day"), (17, "evening"), (22, "night")]

STORIES = {
    "morning": [
        [  # waking up
            ["Psst... {name}, are you awake yet? ☀️", "Knock knock, {name} 🚪 Is my favorite person awake?"],
            ["If you're still in bed, I don't blame you. But the day is waiting to meet you 😌",
             "Still in bed? Take your time... but not too much, I miss you 😌"],
            ["Stretch, yawn, smile. Yes, the smile is mandatory, {name} 😄",
             "Okay: slow stretch, deep breath, and one big smile for me 😄"],
            ["There it is. The prettiest smile in the world, starting a brand-new day 💛",
             "Perfect. Now the day can officially begin 💛"],
        ],
        [  # breakfast
            ["Coffee or tea this morning, {name}? ☕", "Breakfast check, {name}! Did you eat something? 🍳"],
            ["Whatever you're having, I wish I was sitting across the table from you 🥐",
             "I'm picturing us sharing breakfast right now. You steal my toast, as usual 🍞"],
            ["Sip slowly, and let the warm cup remind you of the warm hug I owe you 🤗",
             "Eat well, okay? I need you full of energy and full of smiles 💪"],
            ["Fueled up and ready? Go be the amazing human I know you are ✨",
             "Now you're ready to take on the world. I'm proud of you already ✨"],
        ],
        [  # last night's dream
            ["Did you dream about me last night, {name}? Be honest 😏",
             "I had the sweetest dream last night, {name}. Guess who was in it? 😏"],
            ["Because I'm pretty sure you were in mine. Again 💭", "Hint: it was you. It's always you 💭"],
            ["We were somewhere quiet, just the two of us, and you were laughing at my silly jokes 🌙",
             "We were walking hand in hand and nothing else in the world mattered 🌙"],
            ["Waking up from that was hard. Good thing the real you is even better 💕",
             "Then I woke up and remembered the real you is even better than the dream 💕"],
        ],
        [  # getting ready
            ["Getting ready for the day, {name}? 👗👔",
             "What are you wearing today, {name}? Not that it matters, you look good in everything 😍"],
            ["Pro tip: the best accessory is that smile of yours 😊",
             "Whatever you pick, add one thing: my love. It goes with everything 😊"],
            ["Don't forget your keys, your phone, and the fact that you're loved 🔑📱❤️",
             "Checklist: keys ✓ phone ✓ knowing someone adores you ✓"],
            ["Now go out there and shine, {name} 🌟", "The world isn't ready for how good you look today 🌟"],
        ],
        [  # sunshine
            ["Look outside, {name}. The sun showed up just for you today 🌞",
             "Did you see the sky this morning, {name}? 🌤"],
            ["Okay, maybe not just for you. But it's definitely trying to compete with you 😌",
             "It looks beautiful, but honestly it's no competition for you 😌"],
            ["Spoiler: it's losing. You're still the brightest thing in my morning ☀️", "You win. You always win ☀️"],
            ["Have the sunniest morning, my love 💛", "Carry that sunshine with you today 💛"],
        ],
    ],
    "day": [
        [  # lunch
            ["Lunch break yet, {name}? 🍱", "Hey {name}, did you eat lunch? Don't you dare skip it 🍱"],
            ["Eat something yummy and think of me with every bite 😋",
             "I'd share my food with you. And I don't share food with anyone 😋"],
            ["Drink some water too! A hydrated {name} is a happy {name} 💧",
             "And water! Your body works hard, treat it well 💧"],
            ["Okay, mom mode off. I just care about you a lot, that's all 🥰",
             "Sorry for nagging. It's just love in a bossy outfit 🥰"],
        ],
        [  # busy day
            ["How's your day going, {name}? 💼", "Busy day, {name}? 💼"],
            ["Whatever's on your plate right now, you've got this 💪",
             "I know you've got a lot going on. You're handling it better than you think 💪"],
            ["And if it gets too much, take a deep breath and remember I'm on your side, always 🫂",
             "If anyone stresses you out, just know I'm silently judging them for you 😤"],
            ["Back to it, superstar. I'll be here cheering ✨", "Go crush the rest of the day. I'm cheering from here ✨"],
        ],
        [  # missing you
            ["Random midday thought: I miss you, {name} 💭",
             "It's the middle of the day and I already miss you, {name} 💭"],
            ["Not in a sad way. In a 'can't wait to see your face' way 🥺",
             "Is it normal to miss someone this much? Asking for me 🥺"],
            ["I keep looking at our photos like they're new 📸",
             "I caught myself smiling at my phone because of you. People are staring 📸"],
            ["Anyway, that's all. Just wanted you to know you're on my mind 💕",
             "Okay, back to pretending to be productive. Still thinking about you though 💕"],
        ],
        [  # reasons I love you
            ["Afternoon reminder: here are a few reasons I love you, {name} 📝",
             "Pop quiz, {name}: do you know why I love you? Let me remind you 📝"],
            ["Reason #1: your laugh. It fixes my worst days 😄",
             "Reason #1: the way you look at me like I'm your favorite person 👀"],
            ["Reason #2: you're kind, even when nobody's watching 🌷",
             "Reason #2: you make ordinary moments feel special 🌷"],
            ["Reason #3: you're you. And that's my favorite thing in the world ❤️",
             "Reasons #3 to infinity: everything else about you ❤️"],
        ],
        [  # daydream date
            ["Let's go on a quick daydream date, {name} 🌴",
             "Close your eyes for 10 seconds, {name}. We're going somewhere 🌴"],
            ["We're at a little café by the sea. You ordered, I'm paying, obviously ☕🌊",
             "Picture this: a quiet beach, two cold drinks, and your head on my shoulder 🌊"],
            ["The breeze is messing up your hair and you still look perfect 🌬",
             "Someone is playing soft music nearby and you start humming along 🎶"],
            ["Okay, date's over. Same thing in real life soon? 😘",
             "Okay, back to reality. But we're doing that for real one day 😘"],
        ],
    ],
    "evening": [
        [  # end of the work day
            ["Is your day finally winding down, {name}? 🌇", "Almost done for the day, {name}? 🌇"],
            ["You worked so hard today. I'm really proud of you 🥇",
             "Whatever happened today, you made it through. That's a win 🥇"],
            ["Time to switch off and be a little lazy. You've earned it 🛋",
             "Now kick off your shoes and relax, you deserve it 🛋"],
            ["If I were there, I'd make you dinner and give you a back rub 💆",
             "I'd give anything to be there right now with a hug and your favorite snack 💆"],
        ],
        [  # sunset
            ["The sun is setting, {name}. Did you catch it? 🌅",
             "Look out the window, {name}. The sky is putting on a show 🌅"],
            ["Pink, orange, gold... it's beautiful, but it reminded me of something even prettier 🎨",
             "All those colors, and I still thought of you first 🎨"],
            ["You, obviously. Did you really think it would be anything else? 😌", "You. The answer is always you 😌"],
            ["Every sunset is one day closer to seeing you again 💞",
             "One more day of loving you. Not a bad way to end it 💞"],
        ],
        [  # dinner
            ["What's for dinner tonight, {name}? 🍝", "Dinner plans, {name}? 🍝"],
            ["If you say instant noodles again, I'm coming over to cook 😤",
             "Whatever it is, I bet it tastes better because you're the one eating it 😋"],
            ["Someday we'll cook together, I'll mess it up, and you'll laugh at me 🍳",
             "Someday it'll be candles, music, and just us. Wait for it 🕯"],
            ["Enjoy your dinner, my love. Save some dessert for me 🍰", "Eat well, okay? And save me a bite 🍰"],
        ],
        [  # how was your day
            ["Tell me about your day, {name}. The good parts and the boring ones 📖",
             "I want to hear everything about your day, {name} 📖"],
            ["Even the boring parts sound interesting when you're the one telling them 🎧",
             "I mean it, every little detail. Your stories are my favorite 🎧"],
            ["And if it was a bad day, I'm here. You can tell me that too 🫶",
             "And if today was rough, let me hold some of it for you 🫶"],
            ["Either way, the day ends with someone loving you. That never changes 💗",
             "Good day or bad day, you're still my favorite person 💗"],
        ],
        [  # plans together
            ["Hey {name}, let's plan something 🗓", "Thinking about our next date, {name} 🗓"],
            ["Movie night, a long walk, or getting lost somewhere new? 🎬",
             "Option A: cozy movie night. Option B: street food adventure. Option C: both 🎬"],
            ["Actually, I don't care where. I just want to be wherever you are 📍",
             "Honestly, anywhere works. You're the plan 📍"],
            ["Start counting down. I already am ⏳💕", "It's a date. I'm already excited ⏳💕"],
        ],
    ],
    "night": [
        [  # bedtime
            ["Getting sleepy, {name}? 🌙", "Time to wind down, {name} 🌙"],
            ["Put the phone down soon, okay? Right after reading my messages 😏",
             "Phone down soon... right after this message, of course 😏"],
            ["Get cozy under the blanket and let today go 🛏",
             "Blanket, pillow, comfy position. Let the day melt away 🛏"],
            ["Sleep tight, my love. I'll be right here when you wake up 💤",
             "Good night, {name}. Dream of something sweet... like me 💤"],
        ],
        [  # stars
            ["Look up if you can, {name}. Are the stars out tonight? ✨", "The stars are out tonight, {name} ✨"],
            ["I'm looking at the same sky. That makes it feel like you're close 🌌",
             "Same sky, same moon, so we're kind of together right now 🌌"],
            ["I made a wish on one of them. Want to know what it was? 🌠",
             "I picked a star and named it after you 🌠"],
            ["It was you. Every wish ends up being you 💫", "It's the brightest one. Obviously 💫"],
        ],
        [  # late-night thoughts
            ["Still up, {name}? Me too 🦉", "Late-night thought, {name}... 🦉"],
            ["The night is quiet, and my mind keeps drifting back to you 🌙",
             "When everything goes quiet, you're the loudest thing in my head 🌙"],
            ["I hope you know how lucky I feel to have you 🍀",
             "I don't say it enough, but you make my life so much better 🍀"],
            ["Okay, sleep now. That's an order from your favorite person 😴",
             "Now get some rest, love. Tomorrow I'll be your first message 😴"],
        ],
        [  # lullaby
            ["Shh... lullaby time for {name} 🎵", "Let me tuck you in from here, {name} 🎵"],
            ["Close your eyes. Breathe in slowly... and out 🌬",
             "Pull the blanket up. Deep breath in... and out 🌬"],
            ["Imagine me playing with your hair until you drift off 🤍",
             "Imagine me right next to you, holding your hand 🤍"],
            ["Sweet dreams, my love. See you in the morning ☀️",
             "Sleep well. Tomorrow starts with me loving you again ☀️"],
        ],
        [  # gratitude
            ["Before the day fully ends, {name}, one thing 🕯", "One last thing before sleep, {name} 🕯"],
            ["Thank you for being you. For your patience, your laugh, your heart 🙏",
             "Thank you for choosing me. Every single day 🙏"],
            ["Whatever tomorrow brings, we'll handle it together 🤝",
             "Tomorrow is a new page, and I want you on every one of them 🤝"],
            ["Goodnight, {name}. I love you more than these messages can say 💖",
             "Rest well, my everything. I love you 💖"],
        ],
    ],
}


def phase_at(hour):
    phase = PHASES[-1][1]
    for start, name in PHASES:
        if hour >= start:
            phase = name
    return phase


def _story(story_id):
    phase, _, index = (story_id or "").partition(":")
    try:
        return STORIES[phase][int(index)]
    except (KeyError, ValueError, IndexError):
        return None


def next_line(story_id, step, used, hour):
    """Continue the current storyline, or start a fresh one that fits the time of day.

    `used` lists story ids already told; stories aren't repeated until every story of the phase is used.
    Returns (template, story_id, step, used) where `step` is the index of the returned line.
    """
    story = _story(story_id)
    if story is None or step >= len(story):
        pool = [f"{phase}:{i}" for phase in [phase_at(hour)] for i in range(len(STORIES[phase]))]
        fresh = [s for s in pool if s not in used]
        if not fresh:
            used = [s for s in used if s not in pool]
            fresh = [s for s in pool if s != story_id] or pool
        story_id, step = random.choice(fresh), 0
        used = used + [story_id]
        story = _story(story_id)
    return random.choice(story[step]), story_id, step, used
