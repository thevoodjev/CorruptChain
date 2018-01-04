import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from corruptchain import cli

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def run(argv):
    buf = io.StringIO()
