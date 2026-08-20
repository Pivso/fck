"""fck -- a mindfulness and wellbeing framework for people who are done.

Every function here is a stress-relief technique borrowed from the wellness
industry and then ruined. Swear at the build, not at your colleagues.

    >>> import fck
    >>> fck.seed(1)
    >>> fck.curse("the deploy")          # doctest: +SKIP
    'The deploy is a fucking festering shitshow and I want it given to the sea.'

Intensity runs 1 (client in the room) to 3 (unhinged). Default is 2.
"""

import functools
import sys

from . import _engine as _e
from . import _lexicon as _lex

__version__ = "0.1.0"
__all__ = [
    "curse", "vent", "affirm", "breathe", "serenity", "rage_quit",
    "stress_ball", "bleep", "seed", "RageQuit",
]

seed = _e.seed


class RageQuit(Exception):
    """Raised by rage_quit(). Catch it if you must, coward."""


def curse(target="this", intensity=2):
    """One expletive-bearing sentence about `target`."""
    return _e.pick(_lex.CURSE, target, intensity)


def vent(about="this", intensity=2, lines=3):
    """A short rant. Escalates, then talks itself down. Returns one string."""
    if lines < 1:
        raise ValueError("you cannot vent zero lines, that is called repression")
    body = _e.sample(_lex.CURSE, lines, about, intensity)
    links = _e.fanout(_lex.ESCALATION, lines - 1, about, intensity)
    out = [body[0]]
    for link, line in zip(links, body[1:]):
        out.append(link)
        out.append(line)
    out.append(_e.pick(_lex.CLOSER, about, intensity))
    return "\n".join(out)


def affirm(target="this", intensity=2):
    """A daily affirmation, as ruined by circumstance."""
    return _e.pick(_lex.AFFIRMATION, target, intensity)


def breathe(target="this", intensity=2, cycles=3):
    """Box breathing, adapted. Returns ordered steps: inhale, hold, exhale per
    cycle, then one closing line."""
    if cycles < 1:
        raise ValueError("zero breathing cycles is just holding your breath")
    steps = []
    for _ in range(cycles):
        steps.append(_e.pick(_lex.INHALE, target, intensity))
        steps.append(_e.pick(_lex.HOLD, target, intensity))
        steps.append(_e.pick(_lex.EXHALE, target, intensity))
    steps.append(_e.pick(_lex.BREATH_CLOSE, target, intensity))
    return steps


def serenity(target="this", intensity=2):
    """The full guided session: breathe, swear, affirm. Prints it, slowly-ish."""
    print("--- fck: guided session ---")
    for step in breathe(target, intensity):
        print(f"  {step}")
    print()
    print(f"  {curse(target, intensity)}")
    print()
    print(f"  {affirm(target, intensity)}")
    print("--- session complete. namaste, you absolute trooper. ---")


def rage_quit(reason="this", intensity=3):
    """Leave, dramatically. Raises RageQuit; it does not kill your process."""
    raise RageQuit(_e.pick(_lex.QUIT, reason, intensity))


def stress_ball(func=None, *, intensity=2, stream=None):
    """Decorator: swears on your behalf when the wrapped function raises, then
    re-raises. It does not swallow the error -- that would be a different sin.

        @stress_ball
        def load_config(): ...
    """
    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                target = f"{fn.__name__}() and its {type(exc).__name__}"
                print(curse(target, intensity), file=stream or sys.stderr)
                raise
        return wrapper
    return decorate(func) if func is not None else decorate


def bleep(text, char="*"):
    """Censor the profanity, keep the rage. For when someone walks past."""
    def censor(match):
        word = match.group(0)
        return word[0] + char * (len(word) - 1)
    return _e.PROFANE_RE.sub(censor, text)
