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
