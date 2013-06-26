"""Classify a step's produced data as clean or one of four degraded kinds.

A degraded source is the origin of taint. Every classification below is a
stated rule applied to fields the trace declared, so the same step always gets
the same class. Only tool steps can be degraded at the source; reason and
answer steps carry taint only by depending on something degraded, which is the
job of taint.py, not this module.

The five classes and their rules:
