# CorruptChain

*Trace how a silent tool failure taints a whole agent run.*

CorruptChain reads an agent trace and answers one question: does the final
answer rest on data that actually worked, or does it trace back to a step
that quietly returned nothing? It builds the data dependency graph, classifies
degraded sources, propagates taint with a reason chain, and prints a verdict.

It is offline and deterministic. A trace is a JSON document on disk; there is
no network access and no wall-clock time in the output.

## What a trace looks like

```json
{
  "question": "Which region had the highest error rate last week?",
  "steps": [
    {"id": "s1", "kind": "tool", "name": "list_regions", "status": "ok",
     "output": "emea, apac, amer", "references": []},
    {"id": "s2", "kind": "tool", "name": "query_metrics", "status": "empty",
     "output": "", "references": ["s1"]}
  ]
