"""Word pools and templates. This module is the actual product; everything
else is plumbing that shuffles it.

House rule for anyone adding entries: targets are situations, objects and
abstractions -- the build, the printer, Tuesday. Never people or groups.
Swearing at a dishwasher is therapy; swearing at a person is just being a prick.

Two invariants the tests enforce, so edit with them in mind:

1. Anything profane added to a plain pool is filtered out of intensity 1
   automatically -- but only if the word is also listed in PROFANE below.
2. Templates must not contain hard profanity as literal text. Use the {blast},
   {holler} and {intensifier} slots, which are tiered by intensity.
"""

# --- tiered slots: chosen by intensity, pinned once per sentence -------------

# The bare swear itself. Pinned per render, so one sentence never wanders
# between registers.
BLAST = {
    1: ["sod", "blast", "dash"],
    2: ["fuck"],
    3: ["fuck"],
}

HOLLER = {
    1: ["SUGAAAAR", "BLAAAAST", "OH BOTHEEEER", "FIDDLESTICKS", "CRIKEY"],
    2: ["FUUUUUCK", "SHIIIIIT", "BOLLOCKS"],
    3: [
        "FUUUUUCK", "FUCKING HELL", "MOTHERFUUUUCK",
        "FUCK EVERYTHING", "FUCK THIS ENTIRE PREMISE",
    ],
}

# Intensity 1: sayable in front of a client. 2: the default. 3: unhinged.
INTENSIFIER = {
    1: [
        "damn", "bloody", "sodding", "flaming", "godforsaken", "wretched",
        "blasted", "confounded", "infernal", "blinking", "ruddy", "thundering",
        "almighty", "blessed",
    ],
    2: [
        "fucking", "shitting", "goddamn", "piss-drenched", "shit-caked",
        "bastard", "arse-backwards", "sodding fucking",
    ],
    3: [
        "absolute fucking", "unholy fucking", "motherfucking",
        "biblically fucking", "catastrophically fucking",
        "apocalyptically fucking", "spectacularly fucking",
        "aggressively fucking", "industrially fucking", "weapons-grade fucking",
    ],
}

# --- plain pools: intensity 1 draws from these with PROFANE words removed ----

ADJ = [
    "festering", "greasy", "clapped-out", "half-arsed", "gormless", "wheezing",
    "malignant", "soggy", "brain-dead", "leaking", "haunted", "cursed",
    "flavourless", "unwashed", "sputtering", "concussed", "incontinent",
    "mildewed", "load-bearing", "self-inflicted", "gelatinous", "clammy",
    "weeping", "crumbling", "lopsided", "undercooked", "overcooked",
    "radioactive", "feral", "rancid", "waterlogged", "moth-eaten",
    "sun-bleached", "arthritic", "wall-eyed", "jaundiced", "bloated",
    "threadbare", "sticky", "tepid", "congealed", "ill-advised", "unlicensed",
    "unsupervised", "doomed", "ill-omened", "decrepit", "fossilised",
    "vestigial", "malformed", "off-brand", "knock-off", "expired",
    "discontinued", "actuarially unsound", "structurally optimistic",
    "aggressively mediocre", "confidently wrong", "unratified", "spiteful",
    "vindictive", "smug", "damp",
]

NOUN = [
    "shitshow", "dumpster fire", "clown car", "tyre fire", "trainwreck",
    "abomination", "clusterfuck", "bin fire", "hostage situation", "gremlin",
    "goblin", "turnip", "sack of hammers", "wet sock", "bag of arse",
    "cry for help", "punishment from God", "crime against nature",
    "insult to plumbing", "group project", "war on competence",
    "argument with a wall", "cursed artefact", "haunted spreadsheet",
    "wasp nest", "house of cards", "bag of cats", "sinking barge",
    "burning caravan", "unlicensed carnival ride", "chain letter",
    "ransom note", "plague ship", "tax audit", "root canal", "parking fine",
    "jury summons", "hex", "omen", "cautionary tale", "warning label",
    "safety violation", "health code violation", "structural liability",
    "insurance claim", "monument to hubris", "cathedral of nonsense",
    "pyramid scheme", "wet paper bag", "damp sandwich", "warm beer",
    "flat tyre", "dial tone", "busy signal", "error message with feelings",
    "committee decision", "unfinished basement", "riddle with no answer",
    "letter from the council", "smell in a car",
]

FATE = [
    "launched into the sun", "buried at a crossroads", "fed into a woodchipper",
    "deleted from history", "given to the sea",
    "set on fire and then set on fire again", "salted and forgotten",
    "put down humanely", "sealed in concrete", "launched into low orbit",
    "fed to something larger", "struck from the record", "dissolved in vinegar",
    "returned to sender", "exorcised", "decommissioned without ceremony",
    "buried under a motorway", "folded into a black hole", "quietly euthanised",
    "scattered at sea", "entombed", "redacted", "forgotten by history",
    "recycled into something useful for once",
]

PUNISHMENT = [
    "made to explain it to their mother",
    "forced to live inside their own documentation",
    "denied hot water for the rest of their life",
    "stuck in a middle seat forever",
    "made to use it daily, in front of an audience",
    "banned from keyboards",
    "sentenced to dial-up",
    "made to read every line of it aloud",
    "given a pager that only rings at 3am",
    "forced to maintain it personally, forever",
    "made to attend every meeting about it",
    "cursed with permanently slow wifi",
    "made to answer their own support tickets",
    "given only a trackpad",
    "denied dark mode",
    "made to work in a font they hate",
    "forced to explain it to auditors",
    "sentenced to a lifetime of CAPTCHAs",
    "given a phone stuck at three percent battery",
    "made to sit with what they have done",
]

ALTERNATIVE = [
    "learned the cello", "grown a tomato", "seen my family",
    "walked to another country", "become a person with hobbies",
    "read an actual book", "slept", "developed a personality",
    "learned a language", "built a shed", "made bread",
    "watched the sun move across a wall", "called my mother", "gone outside",
    "learned to swim", "planted something", "finished a jigsaw",
    "taken up pottery", "aged gracefully", "done literally anything else",
]

DURATION = [
    "three hours", "an entire morning", "the best years of my life",
    "an unrecoverable portion of my one and only life", "since Tuesday",
    "longer than my last relationship", "two full days", "most of a decade",
    "a meaningful chunk of my finite lifespan",
    "every waking hour since Thursday", "an afternoon I will never get back",
    "the whole weekend", "forty minutes that felt like Lent", "all of Q3",
]

DISMISSAL = [
    "fucked", "in the bin", "in the sea", "on its knees", "absolutely bent",
    "right in the sea", "binned", "shelved permanently", "told",
    "absolutely stuffed", "in the skip", "buried", "dropped",
    "thoroughly sorted", "escorted from the premises",
]

# --- templates ---------------------------------------------------------------
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
    "{Target} was designed by someone who has never met a {noun}.",
    "If {target} were a {adj} {noun}, that would be an improvement.",
    "I have looked directly at {target} and it looked back.",
    "{Target} is what happens when a {adj} {noun} is given a budget.",
    "Every day I wake up and {target} is still there, {adj} and unrepentant.",
    "{Target} has never once worked and yet somehow has opinions.",
    "{Blast} {target}, {blast} its author, and {blast} the horse it rode in on.",
    "The only good thing about {target} is that one day I will be dead.",
    "{Target} should be studied by science, and then {fate}.",
    "On a scale of one to {noun}, {target} is a {adj} {noun}.",
    "I would rather negotiate with a {adj} {noun} than open {target} again.",
    "{Target} is held together by hope and a {adj} {noun}.",
    "Somebody was paid actual money to make {target}. Money that exists.",
    "Give me {duration} and a hammer and {target} will be {fate}.",
    "I have made peace with many things. {Target} is not one of them.",
    "{Target} is a {intensifier} {adj} {noun} impersonating a solution.",
    "{Target} is the reason the {noun} was invented, and it is still not enough.",
    "Nothing about {target} had to be this way. Somebody chose this.",
]

ESCALATION = [
    "And another thing.",
    "No, I'm not finished.",
    "Actually, while we're here:",
    "But it gets worse.",
    "Sorry, one more.",
    "Related:",
    "Also, and I cannot stress this enough:",
    "One more and then I'll stop:",
    "I lied, I'm not done:",
    "While I have the floor:",
    "Hold on, it compounds:",
    "And let the record show:",
    "Building on that:",
    "Which brings me neatly to:",
    "In addition, and finally, and I mean it this time:",
]

CLOSER = [
    "Anyway. I'm fine. I'm totally fine.",
    "There. Better. Marginally.",
    "Right. Back to it, I suppose.",
    "I feel nothing now, which is progress.",
    "Thank you for coming to my breakdown.",
    "Okay. Deep breath. Onwards.",
    "That is the poison out.",
    "I am going to go and be normal now.",
    "Right. Where were we.",
    "Session adjourned.",
    "I have said my piece and I feel worse.",
    "Let us never speak of this again.",
    "Anyway. Love and light.",
    "I am at peace. Visibly, I am at peace.",
    "And with that, I return to work as though nothing happened.",
]

AFFIRMATION = [
    "You are doing your best. Your best is {adj} {noun} today. That is allowed.",
    "You cannot control {target}. You can only say '{blast} {target}' with your entire chest.",
    "Inhale calm. Exhale a noise like a kettle full of wasps.",
    "You are not behind. You are exactly where you are meant to be, which is unfortunately here.",
    "Nobody is coming to save you, but you are extremely good at swearing, and that counts.",
    "Your worth is not your output. Your output is a {adj} {noun} regardless.",
    "Be gentle with yourself. Be absolutely vile about {target}.",
    "You contain multitudes. Several of them want {target} {fate}.",
    "Progress is not linear. Today it is a {adj} {noun}.",
    "You are allowed to rest. You are allowed to seethe. Ideally both.",
    "Comparison is the thief of joy. {Target} is the thief of everything else.",
    "Let go of what you cannot change. Keep {target} in a jar for later.",
    "Speak to yourself as you would to a friend. Speak of {target} as you would to a wasp.",
    "You are enough. {Target} is far too much.",
    "Honour your feelings. Your feelings are a {adj} {noun} and they are valid.",
    "This too shall pass. {Target} shall pass like a kidney stone.",
    "You have survived one hundred percent of your worst days, largely out of spite.",
    "Set boundaries. Set them on fire if {target} crosses them.",
]

INHALE = [
    "In through the nose, four counts. Picture {target}.",
    "Breathe in, four counts. Think of {target}, in detail.",
    "Fill the lungs, four counts. Let {target} take up space.",
    "In, four counts. Nose only. {Target} does not deserve your mouth.",
    "Inhale for four. Somewhere out there, {target} continues to exist.",
]

HOLD = [
    "Hold it, four counts. Really let it fester.",
    "Hold, four counts. Let the resentment marinate.",
    "Hold. Four counts. Sit in it.",
    "Hold for four. Feel it curdle.",
    "Hold, four counts. This is the part where it turns.",
]

EXHALE = [
    "Out through the mouth, eight counts. The exhale is the word {holler}. All of it.",
    "Out, eight counts. The exhale is {holler}, sustained, until the lungs give up.",
    "Release for eight. The sound you are making is {holler}.",
    "Out, eight counts, and the sound is {holler}. Let the neighbours hear.",
    "Exhale for eight. It comes out as {holler}. This is correct.",
]

BREATH_CLOSE = [
    "Notice the tension in your jaw. Name it. Its name is {target}.",
    "Release. Or do not. It is your body.",
    "Good. You are still furious, but rhythmically.",
    "Return to the room. {Target} is still there. You are simply oxygenated now.",
    "Open your eyes. Nothing has changed, but you have made a noise about it.",
    "Rest here a moment. Then go and be reasonable at people.",
    "Notice how nothing is fixed. Notice how you feel slightly better anyway.",
]

QUIT = [
    "I am out. {Target} can be {fate}. Do not follow me.",
    "That is it. That is the last {noun} I am eating today.",
    "Downing tools. {Target} is a {intensifier} {adj} {noun} and I have a life.",
    "No. Absolutely not. {Target} can get {dismissal} without me.",
    "I am closing the lid. {Target} will still be a {adj} {noun} tomorrow.",
    "Right, I am done. Somebody else can hold {target}.",
    "Logging off. {Target} has taken {duration} and it is not having any more.",
    "I resign from {target}, effective this second, with no notice period.",
    "Finished. {Target} can be {fate} and I will send flowers to nobody.",
]

# Bleeped by bleep(), and stripped out of the intensity 1 pools. Every profane
# word used anywhere in this file must be listed here or tier 1 will leak.
PROFANE = {
    "fuck", "fucks", "fucked", "fucking", "fucker", "fuckers", "clusterfuck",
    "shit", "shits", "shitting", "shitshow", "bullshit", "shite",
    "piss", "pissing", "arse", "arsed", "bastard", "bollocks", "wank",
    "wanker", "cunt", "prick", "dick", "twat", "bitch", "damn", "goddamn",
    "bugger", "bellend", "knobhead", "tosser", "arsehole", "shithouse",
}
