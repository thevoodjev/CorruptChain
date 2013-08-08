"""Parse an agent trace into ordered steps with inputs, outputs, and references.

A trace is a JSON document. The top level object has two keys:

    question   the user question the run is trying to answer, a string
    steps      an ordered list of step objects

Each step object has these fields:

    id         a short unique string identifier, for example "s1"
    kind       one of "tool" or "reason" or "answer"
    tool       the tool name when kind is "tool", otherwise omitted
    status     the raw status a tool reported, for example "ok", "error",
               "empty", "truncated", "partial". Only meaningful for tool steps.
    references a list of step ids this step explicitly declared it consumed.
               These are the declared dependency edges.
    output     the step's produced value, a string. May be empty.
    result_count  an optional integer the tool reported, used by the empty and
               partial rules in degraded.py.
    expected_count an optional integer for what a complete result would hold,
               used by the partial rule.

The final step, the one whose kind is "answer", is the run's final answer.

Parsing is strict: unknown top level keys and unknown step kinds raise
TraceError, because a silently ignored field is exactly the class of defect
this tool exists to catch. Ordering is preserved as written; ids must be
unique. No wall-clock time and no randomness enter the parse, so the same trace
always yields the same Trace.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

VALID_KINDS = ("tool", "reason", "answer")

# Statuses a tool step may carry. "ok" is the only clean one; the rest are the
# degradation signals degraded.py classifies.
VALID_STATUSES = ("ok", "error", "empty", "truncated", "partial")

_TOP_KEYS = {"question", "steps"}
_STEP_KEYS = {
    "id", "kind", "tool", "status", "references", "output",
    "result_count", "expected_count",
}


class TraceError(ValueError):
    """Raised when a trace document is malformed."""


@dataclass(frozen=True)
class Step:
    """One step in an agent run."""

    id: str
    kind: str
    tool: str | None
    status: str | None
    references: tuple[str, ...]
    output: str
    result_count: int | None
    expected_count: int | None

    @property
    def is_answer(self) -> bool:
        return self.kind == "answer"

    @property
    def is_tool(self) -> bool:
        return self.kind == "tool"


@dataclass(frozen=True)
class Trace:
    """A parsed agent run."""

    question: str
    steps: tuple[Step, ...]
    _index: dict[str, Step] = field(default_factory=dict, compare=False)

    def by_id(self, step_id: str) -> Step:
        try:
            return self._index[step_id]
        except KeyError:
            raise TraceError(f"unknown step id: {step_id!r}") from None
