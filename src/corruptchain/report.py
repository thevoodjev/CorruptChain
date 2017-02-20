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


def render_graph(trace: Trace, graph: Graph) -> list[str]:
    """Every edge, labelled declared or inferred, plus a count summary."""
    lines = [f"question: {trace.question}", f"steps: {len(trace.steps)}", ""]
    lines.append("edges (source -> consumer, how):")
    if not graph.edges:
        lines.append("  none")
    for edge in graph.edges:
        lines.append(f"  {edge.source} -> {edge.consumer}  [{edge.how}]")
