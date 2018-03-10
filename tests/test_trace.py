import unittest

from corruptchain import trace


class TestTraceParse(unittest.TestCase):
    def test_minimal_valid(self):
        t = trace.parse('{"question": "q", "steps": []}')
        self.assertEqual(t.question, "q")
        self.assertEqual(t.steps, ())
        self.assertIsNone(t.answer)

    def test_parses_step_fields(self):
        doc = (
            '{"question": "q", "steps": ['
            '{"id": "s1", "kind": "tool", "tool": "grep", "status": "ok",'
            ' "references": [], "output": "hit", "result_count": 1}]}'
        )
        t = trace.parse(doc)
        s = t.by_id("s1")
        self.assertTrue(s.is_tool)
        self.assertEqual(s.tool, "grep")
        self.assertEqual(s.result_count, 1)

    def test_answer_is_last_answer_step(self):
        doc = (
            '{"question": "q", "steps": ['
            '{"id": "a", "kind": "answer", "output": "x"}]}'
        )
        t = trace.parse(doc)
        self.assertIsNotNone(t.answer)
        self.assertEqual(t.answer.id, "a")

    def test_unknown_top_key_rejected(self):
        with self.assertRaises(trace.TraceError):
            trace.parse('{"question": "q", "steps": [], "extra": 1}')

    def test_unknown_step_key_rejected(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "reason", "bogus": 1}]}')
        with self.assertRaises(trace.TraceError):
            trace.parse(doc)

    def test_invalid_kind_rejected(self):
        doc = '{"question": "q", "steps": [{"id": "s1", "kind": "wat"}]}'
        with self.assertRaises(trace.TraceError):
            trace.parse(doc)

    def test_invalid_status_rejected(self):
        doc = ('{"question": "q", "steps": ['
               '{"id": "s1", "kind": "tool", "status": "weird"}]}')
        with self.assertRaises(trace.TraceError):
