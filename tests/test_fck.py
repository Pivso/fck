import io
import unittest

import fck
from fck import _engine, _lexicon


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
        """Escalation pool is small; a long rant must not silently lose curses."""
        fck.seed(11)
        n = len(_lexicon.ESCALATION) + 4
        self.assertEqual(len(fck.vent("x", lines=n).splitlines()), n * 2)

    def test_vent_rejects_zero_lines(self):
        with self.assertRaises(ValueError):
            fck.vent("x", lines=0)

    def test_breathe_is_ordered_in_hold_out(self):
        fck.seed(2)
        steps = fck.breathe("x", cycles=2)
        self.assertEqual(len(steps), 2 * 3 + 1)
        for cycle in range(2):
            inhale, hold, exhale = steps[cycle * 3:cycle * 3 + 3]
            self.assertIn(inhale, [t.replace("{target}", "x") for t in _lexicon.INHALE])
            self.assertTrue(hold.lower().startswith("hold"))
            self.assertTrue(exhale.lower().startswith("out"))

    def test_breathe_rejects_zero_cycles(self):
        with self.assertRaises(ValueError):
            fck.breathe("x", cycles=0)

    def test_intensity_one_is_safe_for_work(self):
        """The whole point of tier 1: no hard profanity, ever."""
        hard = ("fuck", "shit", "piss", "cunt", "arse", "bollocks", "wank")
        fck.seed(0)
        for _ in range(300):
            for text in (fck.curse("x", 1), fck.affirm("x", 1),
                         fck.vent("x", 1), " ".join(fck.breathe("x", 1))):
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
