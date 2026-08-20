"""Template filling. Small on purpose: pick a template, fill its slots, tidy up."""

import random
import re

from . import _lexicon as lex

_SLOT = re.compile(r"\{(\w+)\}")
_A_BEFORE_VOWEL = re.compile(r"\ba (?=[aeiouAEIOU])")

_rng = random.Random()

# Intensity-tiered slots: pinned once per sentence so register stays consistent.
_TIERED = {
    "intensifier": lex.INTENSIFIER,
    "blast": lex.BLAST,
    "holler": lex.HOLLER,
}

_POOLS = {
    "adj": lex.ADJ,
    "noun": lex.NOUN,
    "fate": lex.FATE,
    "punishment": lex.PUNISHMENT,
    "alternative": lex.ALTERNATIVE,
    "duration": lex.DURATION,
    "dismissal": lex.DISMISSAL,
}

PROFANE_RE = re.compile(
    r"\b(?:%s)\b" % "|".join(sorted(map(re.escape, lex.PROFANE), key=len, reverse=True)),
    re.IGNORECASE,
)


def has_profanity(text):
    return bool(PROFANE_RE.search(text))


# Intensity 1 must be sayable with a client in the room, so it draws from the
# same pools with the profanity strained out. Derived, not hand-maintained:
# add a filthy word to a pool and tier 1 stays clean automatically.
_MILD = {
    name: [w for w in pool if not has_profanity(w)] for name, pool in _POOLS.items()
}


def seed(value):
    """Pin the RNG so output is reproducible. Mostly for tests and grudges."""
    _rng.seed(value)


def clamp(intensity):
    return max(1, min(3, int(intensity)))


def fill(template, target, intensity, rng=None):
    """Resolve {slots} in `template`. Capitalised slots capitalise their value."""
    rng = rng or _rng
    intensity = clamp(intensity)
    pinned = {}

    def replace(match):
        key = match.group(1)
        low = key.lower()
        if low == "target":
            value = target
        elif low in _TIERED:
            value = pinned.setdefault(low, rng.choice(_TIERED[low][intensity]))
        else:
            pools = _MILD if intensity == 1 else _POOLS
            value = rng.choice(pools[low])  # KeyError = typo in a template
        return value[:1].upper() + value[1:] if key[0].isupper() else value

    text = template
    for _ in range(4):  # slots can nest; 4 passes is plenty
        if not _SLOT.search(text):
            break
        text = _SLOT.sub(replace, text)
    return _A_BEFORE_VOWEL.sub("an ", text)


def pick(pool, target, intensity, rng=None):
    rng = rng or _rng
    return fill(rng.choice(pool), target, intensity, rng)


def fanout(pool, count, target, intensity, rng=None):
    """`count` lines, preferring distinct templates but repeating once the pool
    runs dry -- a long rant should not lose lines just because it is long."""
    rng = rng or _rng
    out = []
    while len(out) < count:
        need = count - len(out)
        out.extend(rng.sample(pool, min(need, len(pool))))
    return [fill(t, target, intensity, rng) for t in out]


def sample(pool, count, target, intensity, rng=None):
    """`count` distinct templates, or the whole pool shuffled if count is bigger."""
    rng = rng or _rng
    chosen = rng.sample(pool, min(count, len(pool)))
    return [fill(t, target, intensity, rng) for t in chosen]
