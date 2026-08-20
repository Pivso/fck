import contextlib
import io
import re
import unittest

import fck
from fck import _engine, _lexicon


def came_from(text, pool):
    """True if `text` could have been rendered from any template in `pool`.

    Compares structure rather than prefixes, so adding phrasings to a pool
    does not break the ordering tests.
    """
    for template in pool:
        pattern = "^" + re.sub(r"\\\{\w+\\\}", ".+", re.escape(template)) + "$"
        if re.match(pattern, text):
            return True
    return False


class TestTemplates(unittest.TestCase):
    def test_every_template_renders(self):
        """No typo'd slots, no empty pools -- render the lot, many times."""
        pools = [
            _lexicon.CURSE, _lexicon.AFFIRMATION, _lexicon.QUIT,
            _lexicon.ESCALATION, _lexicon.CLOSER, _lexicon.INHALE,
            _lexicon.HOLD, _lexicon.EXHALE, _lexicon.BREATH_CLOSE,
        ]
        for pool in pools:
            self.assertTrue(pool, "empty template pool")
            for template in pool:
                for intensity in (1, 2, 3):
                    out = _engine.fill(template, "the build", intensity)
                    self.assertNotIn("{", out, template)
                    self.assertTrue(out.strip())

    def test_word_pools_are_populated(self):
        for name, pool in _engine._POOLS.items():
            self.assertTrue(pool, f"empty pool: {name}")
        for tier in _engine._TIERED.values():
            for level in (1, 2, 3):
                self.assertTrue(tier[level])

    def test_article_agreement(self):
        out = _engine.fill("It is a {adj} {noun}.", "x", 2)
        self.assertNotRegex(out, r"\ba [aeiou]")

    def test_no_literal_profanity_in_templates(self):
        """Invariant 2: swearing enters via tiered slots, never as literal
        template text -- otherwise it cannot be dialled down for intensity 1."""
        pools = {
            "CURSE": _lexicon.CURSE, "AFFIRMATION": _lexicon.AFFIRMATION,
            "QUIT": _lexicon.QUIT, "ESCALATION": _lexicon.ESCALATION,
            "CLOSER": _lexicon.CLOSER, "INHALE": _lexicon.INHALE,
            "HOLD": _lexicon.HOLD, "EXHALE": _lexicon.EXHALE,
            "BREATH_CLOSE": _lexicon.BREATH_CLOSE,
        }
        for name, pool in pools.items():
            for template in pool:
                bare = re.sub(r"\{\w+\}", "", template)
                self.assertFalse(
                    _engine.has_profanity(bare), f"{name}: {template}"
                )

    def test_mild_pools_keep_enough_variety(self):
        """Tier 1 pools are derived by filtering, so they shrink silently as
        filthier words are added. Guard the floor."""
        for name, pool in _engine._MILD.items():
            self.assertGreaterEqual(len(pool), 10, f"tier-1 pool '{name}' is thin")
            full = len(_engine._POOLS[name])
            self.assertGreaterEqual(
                len(pool), full * 0.5, f"tier-1 pool '{name}' lost half its words"
            )


class TestApi(unittest.TestCase):
    def test_seed_is_reproducible(self):
        fck.seed(42)
        first = [fck.curse("jira"), fck.vent("jira"), fck.affirm("jira")]
        fck.seed(42)
        second = [fck.curse("jira"), fck.vent("jira"), fck.affirm("jira")]
        self.assertEqual(first, second)

    def test_target_appears_or_output_still_works(self):
        fck.seed(7)
        for _ in range(50):
            self.assertTrue(fck.curse("the printer").strip())

    def test_intensity_is_clamped(self):
        self.assertTrue(fck.curse("x", intensity=99).strip())
        self.assertTrue(fck.curse("x", intensity=-4).strip())

    def test_vent_line_count(self):
        fck.seed(3)
        # n curses + (n-1) escalations + 1 closer
        self.assertEqual(len(fck.vent("x", lines=3).splitlines()), 6)
        self.assertEqual(len(fck.vent("x", lines=1).splitlines()), 2)

    def test_long_vent_keeps_every_line(self):
        """Both pools are finite; a long rant must not silently lose lines."""
        fck.seed(11)
        for n in (len(_lexicon.ESCALATION) + 4, len(_lexicon.CURSE) + 12, 100):
            self.assertEqual(len(fck.vent("x", lines=n).splitlines()), n * 2, n)

    def test_vent_rejects_zero_lines(self):
        with self.assertRaises(ValueError):
            fck.vent("x", lines=0)

    def test_breathe_is_ordered_in_hold_out(self):
        fck.seed(2)
        steps = fck.breathe("x", cycles=2)
        self.assertEqual(len(steps), 2 * 3 + 1)
        for cycle in range(2):
            inhale, hold, exhale = steps[cycle * 3:cycle * 3 + 3]
            self.assertTrue(came_from(inhale, _lexicon.INHALE), inhale)
            self.assertTrue(came_from(hold, _lexicon.HOLD), hold)
            self.assertTrue(came_from(exhale, _lexicon.EXHALE), exhale)

    def test_breathe_rejects_zero_cycles(self):
        with self.assertRaises(ValueError):
            fck.breathe("x", cycles=0)

    def test_intensity_one_is_safe_for_work(self):
        """The whole point of tier 1: no hard profanity, ever."""
        hard = ("fuck", "shit", "piss", "cunt", "arse", "bollocks", "wank")
        fck.seed(0)
        for _ in range(300):
            try:
                fck.rage_quit("x", 1)
            except fck.RageQuit as exc:
                quit_line = str(exc)
            for text in (fck.curse("x", 1), fck.affirm("x", 1),
                         fck.vent("x", 1), " ".join(fck.breathe("x", 1)),
                         quit_line):
                low = text.lower()
                for word in hard:
                    self.assertNotIn(word, low, text)

    def test_intensity_three_actually_swears(self):
        fck.seed(0)
        blob = " ".join(fck.curse("x", 3) for _ in range(60)).lower()
        self.assertIn("fuck", blob)

    def test_tiered_slot_is_consistent_within_a_sentence(self):
        """One sentence should not wander between registers."""
        fck.seed(1)
        for _ in range(100):
            out = _engine.fill("{Blast} it. {Blast} it again. {blast}.", "x", 1)
            words = [w.strip(".").lower() for w in out.split()]
            self.assertEqual(len(set(words) - {"it", "again"}), 1, out)

    def test_rage_quit_raises(self):
        with self.assertRaises(fck.RageQuit):
            fck.rage_quit("the sprint")


class TestUntrustedTarget(unittest.TestCase):
    """`target` is caller-supplied and must never be treated as template syntax."""

    def test_braces_in_target_are_kept_literal(self):
        fck.seed(1)
        for probe in ("{noun}", "{adj} {noun}", "{target}", "{Target}"):
            for intensity in (1, 2, 3):
                self.assertIn(probe, fck.curse(probe, intensity))

    def test_unknown_slot_in_target_does_not_raise(self):
        """Ordinary input like "{bogus}" used to raise KeyError."""
        fck.seed(2)
        for _ in range(50):
            self.assertIn("{bogus}", fck.curse("{bogus}"))
        self.assertIn("{bogus}", fck.vent("{bogus}", lines=2))
        self.assertIn("{bogus}", " ".join(fck.breathe("{bogus}")))

    def test_regex_metacharacters_in_target_are_safe(self):
        fck.seed(3)
        for probe in (r"\d+", "(", "[", "$1", "\\", "a" * 500):
            # Compared case-insensitively: a {Target} slot at the start of a
            # sentence legitimately capitalises the first letter.
            self.assertIn(probe.lower(), fck.curse(probe).lower())

    def test_non_string_targets_are_coerced(self):
        fck.seed(4)
        self.assertIn("123", fck.curse(123))
        self.assertIn("None", fck.curse(None))


class TestDeterminism(unittest.TestCase):
    def test_profanity_pattern_is_stable(self):
        """PROFANE is a set; without a tiebreak the pattern varies per process."""
        words = sorted(map(__import__("re").escape, _lexicon.PROFANE),
                       key=lambda w: (-len(w), w))
        self.assertIn("|".join(words), _engine.PROFANE_RE.pattern)


class TestStressBall(unittest.TestCase):
    def test_reraises_and_swears(self):
        stream = io.StringIO()

        @fck.stress_ball(stream=stream)
        def boom():
            raise ValueError("nope")

        with self.assertRaises(ValueError):
            boom()
        self.assertIn("ValueError", stream.getvalue())

    def test_bare_decorator_form(self):
        @fck.stress_ball
        def fine():
            return 1

        self.assertEqual(fine(), 1)

    def test_preserves_metadata(self):
        @fck.stress_ball
        def named(a, b=2):
            """docstring"""
            return a + b

        self.assertEqual(named.__name__, "named")
        self.assertEqual(named.__doc__, "docstring")
        self.assertEqual(named(1), 3)


class TestCli(unittest.TestCase):
    """__main__ is the user-facing surface and had no coverage at all."""

    def run_cli(self, *args):
        from fck.__main__ import main
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main(list(args))
        return code, buf.getvalue()

    def test_default_prints_one_line(self):
        code, out = self.run_cli("the deploy", "--seed", "1")
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 1)
        self.assertIn("the deploy", out)

    def test_seed_makes_output_reproducible(self):
        first = self.run_cli("x", "--seed", "7")[1]
        second = self.run_cli("x", "--seed", "7")[1]
        self.assertEqual(first, second)

    def test_vent_prints_multiple_lines(self):
        _, out = self.run_cli("x", "--vent", "--seed", "2")
        self.assertEqual(len(out.strip().splitlines()), 6)

    def test_breathe_runs_a_session(self):
        _, out = self.run_cli("x", "--breathe", "--seed", "3")
        self.assertIn("guided session", out)
        self.assertIn("session complete", out)

    def test_affirm_flag(self):
        code, out = self.run_cli("x", "--affirm", "--seed", "4")
        self.assertEqual(code, 0)
        self.assertTrue(out.strip())

    def test_bleep_flag_censors(self):
        _, out = self.run_cli("x", "--bleep", "-i", "3", "--seed", "5")
        for word in ("fuck", "shit"):
            self.assertNotIn(word, out.lower())

    def test_intensity_one_is_clean_via_cli(self):
        for seed in range(25):
            _, out = self.run_cli("x", "-i", "1", "--vent", "--seed", str(seed))
            for word in ("fuck", "shit", "arse", "piss"):
                self.assertNotIn(word, out.lower())

    def test_rejects_out_of_range_intensity(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                self.run_cli("x", "-i", "9")

    def test_braces_in_cli_target_are_safe(self):
        code, out = self.run_cli("{bogus}", "--seed", "6")
        self.assertEqual(code, 0)
        self.assertIn("{bogus}", out)


class TestBleep(unittest.TestCase):
    def test_censors_profanity_keeps_shape(self):
        self.assertEqual(fck.bleep("fuck this shit"), "f*** this s***")

    def test_case_insensitive(self):
        self.assertEqual(fck.bleep("FUCK"), "F***")

    def test_leaves_clean_words_alone(self):
        self.assertEqual(fck.bleep("the printer is broken"), "the printer is broken")

    def test_does_not_bleep_substrings(self):
        self.assertEqual(fck.bleep("scunthorpe"), "scunthorpe")


if __name__ == "__main__":
    unittest.main()
