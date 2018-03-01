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
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "error",'
               ' "output": "boom"}]}')
        _, res = analyse(doc)
        self.assertEqual(len(res.origins), 1)
        self.assertEqual(res.origins[0].origin_class, "error")

    def test_declared_forward_propagation(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "empty", "output": ""},'
               '{"id": "s2", "kind": "reason", "references": ["s1"],'
               ' "output": "reasoned"},'
               '{"id": "s3", "kind": "answer", "references": ["s2"],'
               ' "output": "final"}]}')
        _, res = analyse(doc)
        self.assertTrue(res.is_tainted("s2"))
        self.assertTrue(res.is_tainted("s3"))
        rec = res.for_step("s3")
        self.assertEqual(rec.path, ("s1", "s2", "s3"))
        self.assertEqual(rec.weakest_link, "declared")

    def test_inferred_hop_marks_path_weak(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "empty", "output": ""},'
               '{"id": "s2", "kind": "reason", "references": ["s1"],'
               ' "output": "the carried marker phrase"},'
               '{"id": "s3", "kind": "answer",'
               ' "output": "restating the carried marker phrase again"}]}')
        _, res = analyse(doc)
        rec = res.for_step("s3")
        self.assertIsNotNone(rec)
        self.assertEqual(rec.weakest_link, "inferred")

    def test_clean_branch_stays_clean(self):
        doc = ('{"question": "q", "steps": ['
