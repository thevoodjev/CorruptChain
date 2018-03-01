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
