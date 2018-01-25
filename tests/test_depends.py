import unittest

from corruptchain import trace
from corruptchain.depends import DECLARED, INFERRED, build


class TestDepends(unittest.TestCase):
    def test_declared_edge(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "ok",'
               ' "output": "alpha bravo charlie"},'
               '{"id": "s2", "kind": "reason", "references": ["s1"],'
