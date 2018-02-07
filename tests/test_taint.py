import unittest

from corruptchain import trace
from corruptchain.depends import build
from corruptchain.taint import propagate


def analyse(doc):
