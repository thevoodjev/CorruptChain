import unittest

from corruptchain import trace, verdict
from corruptchain.depends import build
from corruptchain.taint import propagate


def judge(doc):
    t = trace.parse(doc)
    g = build(t)
    res = propagate(t, g)
    return verdict.decide(t, res)


class TestVerdict(unittest.TestCase):
    def test_grounded(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "ok",'
               ' "output": "solid working data"},'
               '{"id": "s2", "kind": "answer", "references": ["s1"],'
               ' "output": "final"}]}')
        v = judge(doc)
        self.assertEqual(v.status, verdict.GROUNDED)
        self.assertEqual(v.exit_code, 0)

    def test_tainted(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "empty", "output": ""},'
               '{"id": "s2", "kind": "answer", "references": ["s1"],'
               ' "output": "final"}]}')
        v = judge(doc)
        self.assertEqual(v.status, verdict.TAINTED)
        self.assertEqual(v.origin, "s1")
        self.assertEqual(v.origin_class, "empty")
        self.assertEqual(v.exit_code, 1)

    def test_unknown_without_answer(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "ok",'
               ' "output": "data value here"}]}')
        v = judge(doc)
        self.assertEqual(v.status, verdict.UNKNOWN)
        self.assertIsNone(v.answer_id)
        self.assertEqual(v.exit_code, 0)

    def test_tainted_detail_grammar(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "empty", "output": ""},'
               '{"id": "s2", "kind": "answer", "references": ["s1"],'
               ' "output": "final"}]}')
        v = judge(doc)
        self.assertIn("through a declared path", v.detail)


if __name__ == "__main__":
