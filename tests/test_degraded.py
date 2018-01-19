import unittest

from corruptchain import degraded
from corruptchain.trace import Step


def make(kind="tool", status="ok", output="data here",
         result_count=None, expected_count=None, tool="t"):
    return Step(
        id="x", kind=kind, tool=tool, status=status,
        references=(), output=output,
        result_count=result_count, expected_count=expected_count,
    )


class TestClassify(unittest.TestCase):
    def test_clean_ok_with_output(self):
        self.assertEqual(degraded.classify(make()), degraded.CLEAN)

    def test_error_status(self):
        self.assertEqual(degraded.classify(make(status="error")),
                         degraded.ERROR)

    def test_empty_status(self):
        self.assertEqual(degraded.classify(make(status="empty", output="")),
                         degraded.EMPTY)

    def test_ok_but_no_output_is_empty(self):
        self.assertEqual(degraded.classify(make(status="ok", output="   ")),
                         degraded.EMPTY)

    def test_result_count_zero_is_empty(self):
        self.assertEqual(
            degraded.classify(make(status="ok", output="x", result_count=0)),
            degraded.EMPTY,
        )

    def test_truncated_status(self):
        self.assertEqual(degraded.classify(make(status="truncated")),
                         degraded.TRUNCATED)

    def test_partial_status(self):
        self.assertEqual(degraded.classify(make(status="partial")),
                         degraded.PARTIAL)

    def test_partial_by_counts(self):
        s = make(status="ok", output="x", result_count=2, expected_count=10)
        self.assertEqual(degraded.classify(s), degraded.PARTIAL)

    def test_full_counts_are_clean(self):
        s = make(status="ok", output="x", result_count=10, expected_count=10)
        self.assertEqual(degraded.classify(s), degraded.CLEAN)
