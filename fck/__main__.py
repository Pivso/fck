"""python -m fck "the deploy" --vent -i 3"""

import argparse
import sys

import fck


def main(argv=None):
    p = argparse.ArgumentParser(prog="fck", description="Stress relief. Command line.")
    p.add_argument("target", nargs="?", default="this", help="what has wronged you")
    p.add_argument("-i", "--intensity", type=int, default=2, choices=(1, 2, 3))
    p.add_argument("--vent", action="store_true", help="a full rant, not one line")
    p.add_argument("--breathe", action="store_true", help="guided session")
    p.add_argument("--affirm", action="store_true", help="a daily affirmation")
    p.add_argument("--bleep", action="store_true", help="censor it, boss incoming")
    p.add_argument("--seed", type=int, help="reproducible outrage")
    args = p.parse_args(argv)

    if args.seed is not None:
        fck.seed(args.seed)

    if args.breathe:
        fck.serenity(args.target, args.intensity)
        return 0
    if args.affirm:
        out = fck.affirm(args.target, args.intensity)
    elif args.vent:
        out = fck.vent(args.target, args.intensity)
    else:
        out = fck.curse(args.target, args.intensity)

    print(fck.bleep(out) if args.bleep else out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
