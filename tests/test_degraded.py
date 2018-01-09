import unittest

from corruptchain import degraded
from corruptchain.trace import Step


def make(kind="tool", status="ok", output="data here",
