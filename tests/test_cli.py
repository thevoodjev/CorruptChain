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
