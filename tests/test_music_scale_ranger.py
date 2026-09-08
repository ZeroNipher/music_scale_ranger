import unittest

from music_scale_ranger import (
    get_scale_notes,
    get_harmonic_field,
    guess_scales_from_notes,
)


class TestScaleNotes(unittest.TestCase):

    def test_c_major(self):
        notes = get_scale_notes("MajorScale", "C")
        self.assertEqual(
            notes,
            ["C", "D", "E", "F", "G", "A", "B", "C"]
        )

    def test_c_blues(self):
        notes = get_scale_notes("BluesScale", "C")
        self.assertEqual(
            notes,
            ["C", "E-", "F", "G-", "G", "B-", "C"]
        )


class TestHarmonicField(unittest.TestCase):

    def test_c_major_has_seven_triads(self):
        chords = get_harmonic_field("MajorScale", "C", False)
        self.assertEqual(len(chords), 7)

    def test_c_major_has_seven_seventh_chords(self):
        chords = get_harmonic_field("MajorScale", "C", True)
        self.assertEqual(len(chords), 7)


class TestScaleGuessing(unittest.TestCase):

    def test_find_c_major(self):
        results = guess_scales_from_notes(["C", "E", "G"])

        self.assertIn("MajorScale com tônica C", results)


if __name__ == "__main__":
    unittest.main()