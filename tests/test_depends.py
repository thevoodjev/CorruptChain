import unittest

from corruptchain import trace
from corruptchain.depends import DECLARED, INFERRED, build


class TestDepends(unittest.TestCase):
    def test_declared_edge(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "ok",'
               ' "output": "alpha bravo charlie"},'
               '{"id": "s2", "kind": "reason", "references": ["s1"],'
               ' "output": "derived"}]}')
        g = build(trace.parse(doc))
        self.assertEqual(len(g.edges), 1)
        self.assertEqual(g.edges[0].how, DECLARED)
        self.assertEqual((g.edges[0].source, g.edges[0].consumer), ("s1", "s2"))

    def test_inferred_edge_from_value_match(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "ok",'
               ' "output": "the special token value"},'
               '{"id": "s2", "kind": "reason",'
               ' "output": "carrying the special token value onward"}]}')
        g = build(trace.parse(doc))
