import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from corruptchain import cli

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = cli.main(argv)
    return code, buf.getvalue()


class TestCli(unittest.TestCase):
    def test_version(self):
        code, out = run(["version"])
        self.assertEqual(code, 0)
        self.assertIn("corruptchain", out)

    def test_clean_verdict_exit_zero(self):
        code, out = run(["verdict", str(SAMPLES / "clean_trace.json")])
        self.assertEqual(code, 0)
        self.assertIn("grounded", out)

    def test_contaminated_verdict_exit_one(self):
        code, out = run(["verdict", str(SAMPLES / "contaminated_trace.json")])
        self.assertEqual(code, 1)
        self.assertIn("tainted", out)

    def test_graph_lists_inferred_edge(self):
        code, out = run(["graph", str(SAMPLES / "contaminated_trace.json")])
        self.assertEqual(code, 0)
        self.assertIn("inferred", out)
        self.assertIn("s3 -> s5", out)

    def test_taint_shows_full_path_to_answer(self):
        code, out = run(["taint", str(SAMPLES / "contaminated_trace.json")])
        self.assertEqual(code, 0)
        self.assertIn("s2 -> s3 -> s5 -> s6", out)

    def test_missing_file_is_usage_error(self):
        code, _ = run(["verdict", "no_such_file.json"])
        self.assertEqual(code, cli.USAGE_ERROR)

    def test_clean_sample_has_no_taint(self):
        code, out = run(["taint", str(SAMPLES / "clean_trace.json")])
        self.assertEqual(code, 0)
        self.assertIn("0 tainted", out)


if __name__ == "__main__":
    unittest.main()

# draft note 1873
