"""Classify a step's produced data as clean or one of four degraded kinds.

A degraded source is the origin of taint. Every classification below is a
stated rule applied to fields the trace declared, so the same step always gets
the same class. Only tool steps can be degraded at the source; reason and
answer steps carry taint only by depending on something degraded, which is the
job of taint.py, not this module.

The five classes and their rules:

    clean       A tool step whose status is "ok" and whose output is non empty.
                Reason and answer steps are also clean at the source; they
                produce no external data of their own.

    error       status is "error". The tool failed. Its output, if any, is an
                error message, not data.

    empty       status is "empty", or status is "ok" with an empty output, or
                result_count is 0. A tool that returned nothing while reporting
                success is the exact silent hole this project chases.

    truncated   status is "truncated". The tool returned a prefix of a larger
                result and said so. Later steps reasoning on it may be missing
                the part that mattered.

    partial     status is "partial", or result_count and expected_count are
                both present and result_count is less than expected_count. One
                page of several, or a subset of the intended set.

Precedence, applied top to bottom, so a step with several signals gets the most
severe: error, then empty, then truncated, then partial, then clean.
"""

from __future__ import annotations

from corruptchain.trace import Step

CLEAN = "clean"
ERROR = "error"
EMPTY = "empty"
TRUNCATED = "truncated"
PARTIAL = "partial"

DEGRADED_CLASSES = (ERROR, EMPTY, TRUNCATED, PARTIAL)

# One sentence per class, printed in reports so the reason is never implicit.
RULE_TEXT = {
    ERROR: 'status "error": the tool failed and produced no usable data',
    EMPTY: 'empty result: status "empty", or an ok status with no output, '
           'or result_count 0',
    TRUNCATED: 'status "truncated": a prefix of a larger result was returned',
    PARTIAL: 'partial result: status "partial", or result_count below '
             'expected_count',
    CLEAN: "clean: an ok status with a non empty result",
}


def classify(step: Step) -> str:
    """Return the class of a single step in isolation."""
    if not step.is_tool:
        # Non tool steps hold no source data; they cannot be degraded here.
        return CLEAN

    status = step.status

    if status == ERROR:
        return ERROR

    # Empty: an explicit empty status, an ok status that produced nothing, or a
    # reported result count of zero.
    if status == EMPTY:
        return EMPTY
    if status == "ok" and step.output.strip() == "":
        return EMPTY
    if step.result_count == 0:
        return EMPTY

    if status == TRUNCATED:
        return TRUNCATED

    if status == PARTIAL:
        return PARTIAL
    if (step.result_count is not None
