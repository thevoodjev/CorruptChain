"""Render graph, taint, and verdict results as line oriented text.

Every function returns a list of lines so the CLI can join them and so output
diffs cleanly in git. No colour, no wall-clock time, no randomness: the same
result object always renders to the same lines.
"""

from __future__ import annotations

from corruptchain import degraded
from corruptchain.depends import Graph
from corruptchain.taint import TaintResult
from corruptchain.trace import Trace
from corruptchain.verdict import Verdict


