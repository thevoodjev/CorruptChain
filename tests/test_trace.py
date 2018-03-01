import unittest

from corruptchain import trace


class TestTraceParse(unittest.TestCase):
    def test_minimal_valid(self):
        t = trace.parse('{"question": "q", "steps": []}')
