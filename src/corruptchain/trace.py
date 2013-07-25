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

