# fck

[![CI](https://github.com/Pivso/fck/actions/workflows/ci.yml/badge.svg)](https://github.com/Pivso/fck/actions/workflows/ci.yml)

A mindfulness and wellbeing framework for people who are done.

Every function is a stress-relief technique borrowed from the wellness industry
and then thoroughly ruined. No dependencies. Python 3.9+.

**House rule:** swear at the build, the printer, Tuesday. Not at people. The
lexicon contains no slurs and takes no aim at anyone; that is deliberate, and
pull requests that change it will be closed with feeling.

## Install

```bash
pip install mindfck
```

Installed as `mindfck`, imported as `fck`. PyPI considers the name `fck` too
similar to an existing project, so the package on the index wears the longer
name and everything else stays short:

```python
import fck          # not mindfck
```

```bash
fck "the deploy"    # the command is still fck
```

From a checkout instead: `pip install -e .`

## Use

```python
import fck

fck.curse("the deploy")
# 'The deploy is a fucking festering shitshow and I want it given to the sea.'

print(fck.vent("this sprint", lines=3))
# a rant that escalates, then talks itself down

fck.affirm("the migration")
# "You cannot control the migration. You can only say 'fuck the migration' with your entire chest."

fck.serenity("the printer")   # full guided session: breathe, swear, affirm
fck.breathe("jira")           # list of breathing steps
fck.rage_quit("the sprint")   # raises RageQuit. Does not kill your process.
```

Intensity runs `1` (client in the room) to `3` (unhinged). Default `2`.

```python
fck.curse("the build", intensity=1)   # 'damn', 'sodding', 'godforsaken'
fck.curse("the build", intensity=3)   # considerably less employable
```

### Swearing on your behalf

```python
@fck.stress_ball
def load_config():
    raise FileNotFoundError("config.yaml")

load_config()
# stderr: Whoever built load_config() and its FileNotFoundError should be sentenced to dial-up.
# then re-raises FileNotFoundError, because swallowing it would be a different sin
```

### Someone is walking over

```python
fck.bleep(fck.curse("the build"))
# 'The build is a f****** festering s******* and I want it given to the sea.'
```

### Reproducible outrage

```python
fck.seed(42)   # same seed, same rant. For tests and for grudges.
```

## Command line

```bash
fck "the deploy"                 # one line
fck "the deploy" --vent -i 3     # full rant, unhinged
fck "monday" --breathe           # guided session
fck "the build" --bleep          # censored
python -m fck "jira" --seed 42   # works without installing
```

## Tests

```bash
python -m unittest discover -s tests
```
