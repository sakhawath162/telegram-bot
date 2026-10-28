"""Morning storylines for /nonstop: each one is a short chain where every text continues the last.

By default a story is told at 07:00 (wake up), 07:30 (the middle) and 08:00 (send-off for the day).
Each story is a list of steps, and each step is a list of variants (one is picked at random).
`{name}` is replaced with your partner's nickname.
"""
import random

STORIES = [
    [  # waking up
        ["Psst... {name}, are you awake yet? ☀️", "Knock knock, {name} 🚪 Is my favorite person awake?"],
        ["Okay: slow stretch, deep breath, and one big smile for me 😄",
         "Stretch, yawn, smile. Yes, the smile is mandatory, {name} 😄"],
        ["There it is. The prettiest smile in the world, starting a brand-new day 💛",
         "Perfect. Now the day can officially begin. Go get it, my love 💛"],
    ],
    [  # breakfast
        ["Coffee or tea this morning, {name}? ☕", "Breakfast check, {name}! Did you eat something? 🍳"],
        ["Whatever you're having, I wish I was sitting across the table from you 🥐",
         "I'm picturing us sharing breakfast right now. You steal my toast, as usual 🍞"],
        ["Fueled up and ready? Go be the amazing human I know you are ✨",
         "Now you're ready to take on the world. I'm proud of you already ✨"],
    ],
    [  # last night's dream
        ["Did you dream about me last night, {name}? Be honest 😏",
         "I had the sweetest dream last night, {name}. Guess who was in it? 😏"],
        ["Because you were in mine. Somewhere quiet, just the two of us, you laughing at my silly jokes 💭",
         "Hint: it was you. We were walking hand in hand and nothing else mattered 💭"],
        ["Waking up from that was hard. Good thing the real you is even better 💕",
         "Then I woke up and remembered the real you is even better than the dream 💕"],
    ],
    [  # getting ready
        ["Getting ready for the day, {name}? 👗👔",
         "What are you wearing today, {name}? Not that it matters, you look good in everything 😍"],
        ["Pro tip: the best accessory is that smile of yours 😊",
         "Checklist: keys ✓ phone ✓ knowing someone adores you ✓"],
        ["Now go out there and shine, {name} 🌟", "The world isn't ready for how good you look today 🌟"],
    ],
    [  # sunshine
        ["Look outside, {name}. The sun showed up just for you today 🌞",
         "Did you see the sky this morning, {name}? 🌤"],
        ["It's trying really hard to be as bright as you. Spoiler: it's losing 😌",
         "It looks beautiful, but honestly it's no competition for you 😌"],
        ["Have the sunniest morning, my love 💛", "Carry that sunshine with you today 💛"],
    ],
    [  # missing you
        ["Good morning, {name}. First thought of the day? You 💭",
         "Morning, {name}. I've been awake five minutes and I already miss you 💭"],
        ["I caught myself smiling at my phone because of you. Again 📸",
         "Is it normal to miss someone this much before breakfast? Asking for me 🥺"],
        ["Anyway, just wanted you to know you're on my mind. Have a beautiful day 💕",
         "Can't wait to see your face. Until then, have the best day 💕"],
    ],
    [  # reasons I love you
        ["Good morning, {name}! Pop quiz: do you know why I love you? 📝",
         "Morning, {name} 📝 I made a list of reasons I love you"],
        ["Reason #1: your laugh. Reason #2: the way you look at me. Reason #3: your kindness 😄",
         "Your laugh fixes my worst days, and your kindness makes my best ones even better 😄"],
        ["Reasons #4 to infinity: everything else about you ❤️ Have a great day!",
         "Honestly, the list never ends. Go have a great day, my love ❤️"],
    ],
    [  # daydream date
        ["Good morning, {name} 🌴 Close your eyes for 10 seconds. We're going somewhere",
         "Morning, {name}! Let's go on a quick daydream date before the day starts 🌴"],
        ["A little café by the sea. You ordered, I'm paying, obviously ☕🌊",
         "A quiet beach, two warm coffees, and your head on my shoulder 🌊"],
        ["Okay, back to reality. But we're doing that for real one day 😘",
         "Date's over. Same thing in real life soon? 😘"],
    ],
    [  # big day ahead
        ["Good morning, {name}! Big day ahead? 💼", "Morning, {name} 💼 What's on your plate today?"],
        ["Whatever it is, you've got this. You handle things better than you think 💪",
         "If anyone stresses you out today, just know I'm silently judging them for you 😤"],
        ["Go crush it, superstar. I'll be cheering from here ✨",
         "And remember: whatever happens today, someone loves you very much ✨"],
    ],
    [  # planning our next date
        ["Good morning, {name} 🗓 I was thinking about our next date", "Morning, {name}! Let's plan something fun 🗓"],
        ["Movie night, a long walk, or getting lost somewhere new? 🎬",
         "Option A: cozy movie night. Option B: street food adventure. Option C: both 🎬"],
        ["Actually, I don't care where. I just want to be wherever you are 📍 Have a lovely day!",
         "Honestly, anywhere works. You're the plan 📍 Now go have a lovely day!"],
    ],
]


def _story_index(story_id):
    try:
        index = int(story_id)
    except (TypeError, ValueError):
        return None
    return index if 0 <= index < len(STORIES) else None


def next_line(story_id, step, used, last=False):
    """Continue the current storyline, or start a new one if there is none or it has ended.

    `used` lists story numbers already told; stories aren't repeated until every one has been used.
    With last=True, jump to the story's closing line so the morning always ends properly.
    Returns (template, story_id, step, used) where `step` is the index of the returned line.
    """
    index = _story_index(story_id)
    if index is None or step >= len(STORIES[index]):
        fresh = [i for i in range(len(STORIES)) if i not in used]
        if not fresh:
            used = []
            fresh = [i for i in range(len(STORIES)) if i != index] or [0]
        index, step = random.choice(fresh), 0
        used = used + [index]
    story = STORIES[index]
    if last:
        step = len(story) - 1
    return random.choice(story[step]), index, step, used
