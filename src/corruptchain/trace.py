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
