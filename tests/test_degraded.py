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
