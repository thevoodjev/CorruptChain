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

