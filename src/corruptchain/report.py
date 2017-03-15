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
    lines.append("")
    lines.append(
        f"edge count: {len(graph.edges)} "
        f"({len(graph.declared)} declared, {len(graph.inferred)} inferred)"
    )
    return lines


def render_taint(trace: Trace, graph: Graph, taint: TaintResult) -> list[str]:
    """Degraded origins, then every tainted step with its path."""
    lines: list[str] = []

    lines.append("degraded sources:")
    if not taint.origins:
        lines.append("  none")
    for origin in taint.origins:
        step = trace.by_id(origin.step_id)
        tool = step.tool or "?"
        lines.append(
            f"  {origin.step_id} [{origin.origin_class}] tool={tool}: "
            f"{degraded.rule_for(origin.origin_class)}"
        )
    lines.append("")

    origin_ids = {o.step_id for o in taint.origins}
    downstream = [t for t in taint.tainted if t.step_id not in origin_ids]

    lines.append("tainted steps (downstream of a degraded source):")
    if not downstream:
        lines.append("  none")
    for rec in downstream:
        path = " -> ".join(rec.path)
        lines.append(
            f"  {rec.step_id}: via {rec.weakest_link} path  {path}"
        )
    lines.append("")

    lines.append(
        f"taint summary: {len(taint.origins)} degraded, "
        f"{len(taint.tainted)} tainted of {len(trace.steps)} steps"
    )
