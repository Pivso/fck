"""fck -- a mindfulness and wellbeing framework for people who are done.

Every function here is a stress-relief technique borrowed from the wellness
industry and then ruined. Swear at the build, not at your colleagues.

    >>> import fck
    >>> fck.seed(1)
    >>> fck.curse("the deploy")          # doctest: +SKIP
    'The deploy is a fucking festering shitshow and I want it given to the sea.'

Every generator takes the same two arguments:

target      the thing that has wronged you, interpolated into the output.
            A situation or an object -- "the deploy", "Tuesday". Not a person.
intensity   1 contains no profanity at all and is safe to print in front of a
            client; 2 is the default and swears freely; 3 is unhinged. Values
            outside 1-3 are clamped, never rejected.

Output is random unless you call seed() first. Nothing here touches the
filesystem, the network, or the process -- functions return strings, except
serenity() which prints and rage_quit() which raises.
"""

from __future__ import annotations

import functools
import sys
from typing import Callable, TextIO, TypeVar

from . import _engine as _e
from . import _lexicon as _lex

__version__ = "0.1.0"
__all__ = [
    "curse", "vent", "affirm", "breathe", "serenity", "rage_quit",
    "stress_ball", "bleep", "seed", "RageQuit",
]

F = TypeVar("F", bound=Callable[..., object])

seed = _e.seed


class RageQuit(Exception):
    """Raised by rage_quit(). Catch it if you must, coward."""


def curse(target: str = "this", intensity: int = 2) -> str:
    """Return one expletive-bearing sentence about `target`.

    Args:
        target: what has wronged you, e.g. "the deploy".
        intensity: 1 (clean) to 3 (unhinged); out-of-range values are clamped.

    Returns:
        A single sentence. Never empty, never multi-line.
    """
    return _e.pick(_lex.CURSE, target, intensity)


def vent(about: str = "this", intensity: int = 2, lines: int = 3) -> str:
    """Return a rant that escalates, then talks itself down.

    Args:
        about: what has wronged you.
        intensity: 1 (clean) to 3 (unhinged); clamped.
        lines: how many complaints to make. Must be at least 1.

    Returns:
        One newline-joined string of ``lines * 2`` lines: each complaint after
        the first is preceded by a connective, and a closing line is appended.

    Raises:
        ValueError: if `lines` is less than 1.
    """
    if lines < 1:
        raise ValueError("you cannot vent zero lines, that is called repression")
    body = _e.fanout(_lex.CURSE, lines, about, intensity)
    links = _e.fanout(_lex.ESCALATION, lines - 1, about, intensity)
    out = [body[0]]
    for link, line in zip(links, body[1:]):
        out.append(link)
        out.append(line)
    out.append(_e.pick(_lex.CLOSER, about, intensity))
    return "\n".join(out)


def affirm(target: str = "this", intensity: int = 2) -> str:
    """Return a daily affirmation, as ruined by circumstance.

    Args:
        target: what has wronged you.
        intensity: 1 (clean) to 3 (unhinged); clamped.

    Returns:
        A single line of wellness advice that has gone wrong.
    """
    return _e.pick(_lex.AFFIRMATION, target, intensity)


def breathe(target: str = "this", intensity: int = 2, cycles: int = 3) -> list[str]:
    """Return box-breathing instructions, adapted.

    Args:
        target: what to picture while breathing.
        intensity: 1 (clean) to 3 (unhinged); clamped.
        cycles: how many breath cycles. Must be at least 1.

    Returns:
        ``cycles * 3 + 1`` steps in order -- inhale, hold, exhale per cycle,
        then one closing line. Printing them is left to the caller.

    Raises:
        ValueError: if `cycles` is less than 1.
    """
    if cycles < 1:
        raise ValueError("zero breathing cycles is just holding your breath")
    steps = []
    for _ in range(cycles):
        steps.append(_e.pick(_lex.INHALE, target, intensity))
        steps.append(_e.pick(_lex.HOLD, target, intensity))
        steps.append(_e.pick(_lex.EXHALE, target, intensity))
    steps.append(_e.pick(_lex.BREATH_CLOSE, target, intensity))
    return steps


def serenity(target: str = "this", intensity: int = 2) -> None:
    """Print a full guided session: breathe, then curse, then affirm.

    The only function here that writes to stdout. Use breathe(), curse() and
    affirm() directly if you want the strings instead.

    Args:
        target: what has wronged you.
        intensity: 1 (clean) to 3 (unhinged); clamped.
    """
    print("--- fck: guided session ---")
    for step in breathe(target, intensity):
        print(f"  {step}")
    print()
    print(f"  {curse(target, intensity)}")
    print()
    print(f"  {affirm(target, intensity)}")
    print("--- session complete. namaste, you absolute trooper. ---")


def rage_quit(reason: str = "this", intensity: int = 3) -> None:
    """Leave, dramatically, by raising RageQuit.

    Raises an exception rather than exiting: it will not kill your process or
    your interpreter, and it can be caught like anything else.

    Args:
        reason: what drove you to this.
        intensity: 1 (clean) to 3 (unhinged); clamped. Defaults to 3.

    Raises:
        RageQuit: always. That is the entire function.
    """
    raise RageQuit(_e.pick(_lex.QUIT, reason, intensity))


def stress_ball(
    func: F | None = None,
    *,
    intensity: int = 2,
    stream: TextIO | None = None,
) -> F | Callable[[F], F]:
    """Decorate a function so it swears when it raises, then re-raises.

    The exception is never swallowed -- swearing about a problem is not the
    same as handling it. Usable bare or called::

        @stress_ball
        def load_config(): ...

        @stress_ball(intensity=3)
        def deploy(): ...

    Args:
        func: supplied automatically when used bare.
        intensity: 1 (clean) to 3 (unhinged); clamped.
        stream: where to write the curse. Defaults to sys.stderr.

    Returns:
        The wrapped function, with its name, docstring and signature intact.
    """
    def decorate(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                target = f"{fn.__name__}() and its {type(exc).__name__}"
                print(curse(target, intensity), file=stream or sys.stderr)
                raise
        return wrapper  # type: ignore[return-value]
    return decorate(func) if func is not None else decorate


def bleep(text: str, char: str = "*") -> str:
    """Censor the profanity in `text`, keeping the rage and the word shape.

    Whole words only, case-insensitive, first letter preserved: "fuck" becomes
    "f***". Words that merely contain a rude substring are left alone, so
    "scunthorpe" survives.

    Args:
        text: any string, typically the output of another function here.
        char: the masking character.

    Returns:
        The text with known profanity masked. Everything else is untouched.
    """
    def censor(match):
        word = match.group(0)
        return word[0] + char * (len(word) - 1)
    return _e.PROFANE_RE.sub(censor, text)
