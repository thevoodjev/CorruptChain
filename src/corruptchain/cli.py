"""corruptchain command line interface.

Subcommands:

    graph    TRACE    print the dependency graph, declared and inferred edges
    taint    TRACE    print degraded sources and the full taint path
    verdict  TRACE    judge whether the final answer is grounded, tainted, or
                      unknown. Exit 1 when the answer is tainted.
    version           print the version

Exit codes:
    0  clean: no findings, or an informational subcommand succeeded
    1  findings: the final answer is tainted (verdict only)
    2  usage error, or a malformed trace
"""

from __future__ import annotations

import argparse
import sys

from corruptchain import __version__, report
from corruptchain.depends import build
from corruptchain.taint import propagate
from corruptchain.trace import TraceError, load
from corruptchain.verdict import decide

USAGE_ERROR = 2


def _load(path: str) -> "tuple":
    """Load a trace and build the graph and taint, or exit 2 on a bad trace."""
    trace = load(path)
    graph = build(trace)
    taint = propagate(trace, graph)
    return trace, graph, taint


def _cmd_graph(args: argparse.Namespace) -> int:
    trace, graph, _ = _load(args.trace)
    print("\n".join(report.render_graph(trace, graph)))
