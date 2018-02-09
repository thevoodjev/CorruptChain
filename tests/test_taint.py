import unittest

from corruptchain import trace
from corruptchain.depends import build
from corruptchain.taint import propagate


def analyse(doc):
    t = trace.parse(doc)
    g = build(t)
    return t, propagate(t, g)


class TestTaint(unittest.TestCase):
    def test_no_degraded_no_taint(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "ok",'
               ' "output": "good data here"},'
               '{"id": "s2", "kind": "answer", "references": ["s1"],'
               ' "output": "final"}]}')
        _, res = analyse(doc)
        self.assertEqual(res.origins, ())
        self.assertEqual(res.tainted, ())

    def test_origin_seeded(self):
