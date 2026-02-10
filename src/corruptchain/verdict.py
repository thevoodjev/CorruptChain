"""Decide whether the final answer was derived from working data.

Three verdicts, and the rule for each:

    grounded   The trace has a final answer step and it is not tainted. Every
               source it depends on classified clean, so the answer rests on
               working data.

    tainted    The final answer is tainted: it depends, directly or through
               other steps, on at least one degraded source. The answer may
               still read as confident prose, which is the danger; it was built
               partly on a hole.

    unknown    The trace declares no final answer step, so there is nothing to
               judge. We refuse to guess a verdict rather than invent one.

A tainted verdict also reports whether the taint path to the answer was carried
entirely by declared edges or leaned on an inferred value match, because that
changes how strongly the contamination is established.
"""

from __future__ import annotations

from dataclasses import dataclass

from corruptchain.taint import TaintResult
from corruptchain.trace import Trace

GROUNDED = "grounded"
TAINTED = "tainted"
UNKNOWN = "unknown"


@dataclass(frozen=True)
class Verdict:
    """The judgement on a run's final answer."""

    status: str            # grounded, tainted, or unknown
    answer_id: str | None  # the answer step id, or None when unknown
    origin: str | None     # the degraded source, when tainted
    origin_class: str | None
    evidence: str | None   # "declared" or "inferred" when tainted
    detail: str            # one line explaining the verdict

    @property
    def exit_code(self) -> int:
        # 1 signals findings present: the answer cannot be trusted.
        return 1 if self.status == TAINTED else 0


def decide(trace: Trace, taint: TaintResult) -> Verdict:
    answer = trace.answer
    if answer is None:
        return Verdict(
            status=UNKNOWN,
            answer_id=None,
            origin=None,
            origin_class=None,
            evidence=None,
            detail="trace declares no final answer step, nothing to judge",
        )

    record = taint.for_step(answer.id)
    if record is None:
        return Verdict(
            status=GROUNDED,
            answer_id=answer.id,
            origin=None,
            origin_class=None,
            evidence=None,
            detail="final answer depends only on clean sources",
        )

    return Verdict(
        status=TAINTED,
        answer_id=answer.id,
        origin=record.origin,
        origin_class=record.origin_class,
        evidence=record.weakest_link,
        detail=(
            f"final answer traces to {record.origin_class} source "
            f"{record.origin!r} through an {record.weakest_link} path"
            if record.weakest_link == "inferred"
            else f"final answer traces to {record.origin_class} source "
                 f"{record.origin!r} through a declared path"
        ),
    )

# draft note 1880
