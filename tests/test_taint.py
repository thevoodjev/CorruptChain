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
