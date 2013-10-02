"""Build the data dependency graph of an agent run.

An edge from step A to step B means B consumed A's output. Edges are found two
ways, and the two are never treated as equal:

    declared   B listed A in its references field. This is the agent stating
               outright that it used A. Strong evidence.

    inferred   B did not list A, but A's output value appears verbatim inside
               B's output. We infer that B carried A's data forward. Weaker
               evidence, because a value can coincide, so it is labelled as an
               inference and never silently promoted to a declared fact.

The honesty rule from the brief lives here: every edge records how it was
established, and a report can list exactly which edges were inferred. When both
a declaration and a value match exist for the same pair, the edge is declared,
because the stronger evidence wins, and the value match is redundant.

Inference is deliberately conservative to avoid false edges:

    - Only outputs of at least MIN_MATCH_LEN characters are matched, so short
      or empty strings never create edges.
    - The match is a substring test against the whole earlier output, trimmed.
    - Only earlier steps can be sources, matching the acyclic order of a run.
"""

from __future__ import annotations

from dataclasses import dataclass

from corruptchain.trace import Trace

DECLARED = "declared"
INFERRED = "inferred"

# Shorter outputs are too likely to collide to support an inferred edge.
MIN_MATCH_LEN = 8


@dataclass(frozen=True)
class Edge:
    """A dependency edge: consumer depends on source."""

    source: str
    consumer: str
    how: str  # DECLARED or INFERRED

    @property
    def is_declared(self) -> bool:
        return self.how == DECLARED


@dataclass(frozen=True)
class Graph:
    """The dependency graph of a trace."""

    edges: tuple[Edge, ...]

    def sources_of(self, consumer: str) -> tuple[Edge, ...]:
        """Edges feeding into a step."""
        return tuple(e for e in self.edges if e.consumer == consumer)

    def consumers_of(self, source: str) -> tuple[Edge, ...]:
        """Edges leaving a step."""
        return tuple(e for e in self.edges if e.source == source)

    @property
    def declared(self) -> tuple[Edge, ...]:
        return tuple(e for e in self.edges if e.how == DECLARED)

    @property
    def inferred(self) -> tuple[Edge, ...]:
        return tuple(e for e in self.edges if e.how == INFERRED)


def build(trace: Trace) -> Graph:
    """Construct the dependency graph, declared edges first, then inferred."""
    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()

    # Declared edges, in trace order, consumer by consumer.
    for step in trace.steps:
        for ref in step.references:
            key = (ref, step.id)
