"""Word pools and templates.

House rule for anyone adding entries: targets are situations, objects and
abstractions -- the build, the printer, Tuesday. Never people or groups.
Swearing at a dishwasher is therapy; swearing at a person is just being a prick.
"""

# Intensity 1: sayable in front of a client. 2: the default. 3: unhinged.
INTENSIFIER = {
    1: ["damn", "bloody", "sodding", "flaming", "godforsaken", "wretched"],
    2: ["fucking", "shitting", "goddamn", "piss-drenched", "shit-caked"],
    3: [
        "absolute fucking",
        "unholy fucking",
        "motherfucking",
        "biblically fucking",
        "catastrophically fucking",
    ],
}

# The bare swear itself, tiered. Resolved once per sentence so a single
# curse doesn't wander between registers mid-breath.
BLAST = {1: ["sod"], 2: ["fuck"], 3: ["fuck"]}

HOLLER = {
    1: ["SUGAAAAR", "BLAAAAST", "OH BOTHEEEER"],
    2: ["FUUUUUCK", "SHIIIIIT"],
    3: ["FUUUUUCK", "FUCKING HELL", "MOTHERFUUUUCK"],
}

ADJ = [
    "festering", "greasy", "clapped-out", "half-arsed", "gormless", "wheezing",
    "malignant", "soggy", "brain-dead", "leaking", "haunted", "cursed",
    "flavourless", "unwashed", "sputtering", "concussed", "incontinent",
    "mildewed", "load-bearing", "self-inflicted", "gelatinous", "clammy",
]

NOUN = [
    "shitshow", "dumpster fire", "clown car", "tyre fire", "trainwreck",
    "abomination", "clusterfuck", "bin fire", "hostage situation", "gremlin",
    "goblin", "turnip", "sack of hammers", "wet sock", "bag of arse",
    "cry for help", "punishment from God", "crime against nature",
    "insult to plumbing", "group project", "war on competence",
    "argument with a wall",
]

FATE = [
    "launched into the sun", "buried at a crossroads", "fed into a woodchipper",
    "deleted from history", "given to the sea", "set on fire and then set on fire again",
    "salted and forgotten", "put down humanely", "sealed in concrete",
]

PUNISHMENT = [
    "made to explain it to their mother",
    "forced to live inside their own documentation",
    "denied hot water for the rest of their life",
    "stuck in a middle seat forever",
    "made to use it daily, in front of an audience",
    "banned from keyboards",
    "sentenced to dial-up",
]

ALTERNATIVE = [
    "learned the cello", "grown a tomato", "seen my family",
    "walked to another country", "become a person with hobbies",
    "read an actual book", "slept", "developed a personality",
]

DURATION = [
    "three hours", "an entire morning", "the best years of my life",
    "an unrecoverable portion of my one and only life", "since Tuesday",
    "longer than my last relationship",
]

DISMISSAL = ["fucked", "in the bin", "in the sea", "on its knees", "absolutely bent"]

# {Capitalised} slots capitalise their result. Slots resolve recursively.
CURSE = [
    "{Target} is a {intensifier} {adj} {noun} and I want it {fate}.",
    "Whoever built {target} should be {punishment}.",
    "{Target}? {Target} can get {dismissal}.",
    "{Blast} {target}. {Blast} it sideways. {Blast} it with a rake.",
    "I have given {duration} to {target}. I could have {alternative}.",
    "{Target} is a {adj} {noun} wearing a {noun} as a hat.",
    "May {target} be {fate}, and may nobody attend the funeral.",
    "There is not enough {intensifier} coffee on this planet for {target}.",
    "{Target} has the structural integrity of a {adj} {noun}.",
    "I would not wish {target} on a {adj} {noun}.",
]

# Connective tissue for a rant, so it escalates instead of listing.
ESCALATION = [
    "And another thing.",
    "No, I'm not finished.",
    "Actually, while we're here:",
    "But it gets worse.",
    "Sorry, one more.",
]

CLOSER = [
    "Anyway. I'm fine. I'm totally fine.",
    "There. Better. Marginally.",
    "Right. Back to it, I suppose.",
    "I feel nothing now, which is progress.",
    "Thank you for coming to my breakdown.",
]

AFFIRMATION = [
    "You are doing your best. Your best is {adj} {noun} today. That is allowed.",
    "You cannot control {target}. You can only say '{blast} {target}' with your entire chest.",
    "Inhale calm. Exhale a noise like a kettle full of wasps.",
    "You are not behind. You are exactly where you are meant to be, which is unfortunately here.",
    "Nobody is coming to save you, but you are extremely good at swearing, and that counts.",
    "Your worth is not your output. Your output is a {adj} {noun} regardless.",
    "Be gentle with yourself. Be absolutely vile about {target}.",
]

INHALE = [
    "In through the nose, four counts. Picture {target}.",
    "Breathe in, four counts. Think of {target}, in detail.",
]

HOLD = [
    "Hold it, four counts. Really let it fester.",
    "Hold, four counts. Let the resentment marinate.",
]

EXHALE = [
    "Out through the mouth, eight counts. The exhale is the word {holler}. All of it.",
    "Out, eight counts. The exhale is {holler}, sustained, until the lungs give up.",
]

BREATH_CLOSE = [
    "Notice the tension in your jaw. Name it. Its name is {target}.",
    "Release. Or don't. It's your body.",
    "Good. You are still furious, but rhythmically.",
]

QUIT = [
    "I'm out. {Target} can be {fate}. Do not follow me.",
    "That's it. That is the last {noun} I am eating today.",
    "Downing tools. {Target} is a {intensifier} {adj} {noun} and I have a life.",
    "No. Absolutely not. {Target} can get {dismissal} without me.",
]

# Bleeped by bleep() when the boss walks past.
PROFANE = {
    "fuck", "fucks", "fucked", "fucking", "fuckers", "clusterfuck",
    "shit", "shits", "shitting", "shitshow", "bullshit",
    "piss", "pissing", "arse", "arsed", "bastard", "bollocks", "wank",
    "cunt", "prick", "dick", "twat", "bitch", "damn", "goddamn",
}
