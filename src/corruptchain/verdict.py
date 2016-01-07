"""Decide whether the final answer was derived from working data.

Three verdicts, and the rule for each:

    grounded   The trace has a final answer step and it is not tainted. Every
               source it depends on classified clean, so the answer rests on
               working data.

