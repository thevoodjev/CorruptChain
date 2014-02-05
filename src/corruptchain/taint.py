"""Forward taint propagation with a reason chain.

Taint originates at degraded sources (degraded.py) and flows forward along
dependency edges (depends.py). A step is tainted when it depends, directly or
transitively, on at least one degraded source. Every tainted step records the
chain of reasons that reached it, so the full path from the silent hole to the
final answer can be printed.

The reason chain is honest about edge strength. Each hop stores whether the
edge that carried the taint was declared or inferred, because a taint path that
runs entirely through declared edges is stronger evidence of contamination than
one that leans on an inferred value match.

Propagation is a breadth first sweep in trace order. The graph is acyclic by
construction (edges only point from earlier steps to later ones), so a single
forward pass settles every step. Determinism holds: identical inputs produce an
identical TaintResult.
"""

from __future__ import annotations

from dataclasses import dataclass

from corruptchain import degraded
from corruptchain.depends import Edge, Graph
from corruptchain.trace import Trace


@dataclass(frozen=True)
class TaintHop:
    """One link in a taint path."""

    source: str        # the step that passed taint on
    via: str | None    # the edge kind that carried it, or None at the origin
    reason: str        # human readable reason for this hop


@dataclass(frozen=True)
class TaintedStep:
    """A step reached by taint, with the origin and the path that reached it."""

    step_id: str
    origin: str          # the degraded source this taint traces back to
    origin_class: str    # error, empty, truncated, or partial
    path: tuple[str, ...]  # step ids from origin to this step, inclusive
    weakest_link: str    # "declared" if every hop was declared, else "inferred"


@dataclass(frozen=True)
class TaintResult:
    """The outcome of propagating taint across a trace."""

    origins: tuple[TaintedStep, ...]   # the degraded sources themselves
    tainted: tuple[TaintedStep, ...]   # every tainted step, origins included

    def is_tainted(self, step_id: str) -> bool:
        return any(t.step_id == step_id for t in self.tainted)

    def for_step(self, step_id: str) -> TaintedStep | None:
        for t in self.tainted:
            if t.step_id == step_id:
                return t
        return None


