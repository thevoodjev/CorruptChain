import unittest

from corruptchain import trace, verdict
from corruptchain.depends import build
from corruptchain.taint import propagate


def judge(doc):
    t = trace.parse(doc)
    g = build(t)
    res = propagate(t, g)
    return verdict.decide(t, res)
