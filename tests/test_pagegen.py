import unittest

from pagegen import extract_title


class TestPageGen(unittest.TestCase):
    def test_extract_title(self):
        md = "# hello\n\ni'm robocop"
        self.assertEqual(extract_title(md), "hello")

        md = "# hi guys\n\ni'm robocop"
        self.assertEqual(extract_title(md), "hi guys")

        md = "## hi\n\ni'm robocop"
        self.assertRaises(Exception, lambda: extract_title(md))

        md = " # hi\n\ni'm robocop"
        self.assertRaises(Exception, lambda: extract_title(md))

        md = "i'm robocop"
        self.assertRaises(Exception, lambda: extract_title(md))
