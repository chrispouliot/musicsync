from unittest import TestCase

from musicsync.utils import is_match


class TestUtils(TestCase):
    def test_perfect_match(self):
        self.assertTrue(is_match("perfect", "perfect"))

    def test_incorrect_match(self):
        self.assertFalse(is_match("wrong", "bad"))

    def test_barely_match(self):
        self.assertTrue(is_match("match", "amatcha"))
