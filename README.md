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
}
```

Each step declares an id, a kind, a status, and the ids it consumed in
`references`. The parser is strict about structure and names the field when a
step is malformed.

## Commands

| Command | What it prints |
|---|---|
| `graph` | the dependency graph with declared and inferred edges |
| `taint` | degraded sources and the full taint path to every affected step |
| `verdict` | grounded, tainted, or unknown, for the final answer step |
| `version` | the version string |

Exit codes: `0` clean or grounded, `1` tainted, `2` usage or parse error.

## Declared is not inferred

An edge from step A to step B means B consumed A's output. CorruptChain finds
edges two ways and never treats them as equal:

- **declared** - B listed A in its `references`. The agent is stating outright
  that it used A. Strong evidence.
- **inferred** - B did not list A, but A's output value appears verbatim inside
  B's output. Weaker evidence: a coincidence in formatting is possible.

Every taint path records, hop by hop, whether the edge that carried the taint
was declared or inferred, so a reader can weigh the path.

## A real run

`python -m corruptchain taint samples/contaminated_trace.json`:

```
degraded sources:
  s2 [empty] tool=query_metrics: empty result: status "empty", or an ok status with no output, or result_count 0

tainted steps (downstream of a degraded source):
  s3: via declared path  s2 -> s3
  s5: via inferred path  s2 -> s3 -> s5
  s6: via inferred path  s2 -> s3 -> s5 -> s6

taint summary: 1 degraded, 4 tainted of 6 steps
```

`python -m corruptchain verdict samples/contaminated_trace.json` (exit 1):

```
verdict: tainted
answer step: s6
origin: s2 [empty]
evidence: inferred path
detail: final answer traces to empty source 's2' through an inferred path
```

The same command on `samples/clean_trace.json` prints `verdict: grounded` and
exits 0: every source the answer depends on classified clean.

## The graph

`python -m corruptchain graph samples/contaminated_trace.json`:

```
question: Which region had the highest error rate last week, and by how much?
steps: 6

edges (source -> consumer, how):
  s1 -> s2  [declared]
  s2 -> s3  [declared]
  s1 -> s4  [declared]
  s4 -> s5  [declared]
  s5 -> s6  [declared]
  s3 -> s5  [inferred]

edge count: 6 (5 declared, 1 inferred)
```

## Degraded sources

A degraded source is the origin of taint: a tool step whose produced data is
not usable. Each class is a stated rule applied to fields the trace declared,
so the same step always gets the same classification. `empty` is the most
common in practice: a tool reports success but returns nothing a consumer can
use. Only tool steps can be degraded at the source; reason and answer steps
carry taint only by depending on something degraded.

## Verdicts

| Verdict | Rule |
|---|---|
| grounded | the final answer step exists and is not tainted |
| tainted | the final answer depends, directly or transitively, on a degraded source |
| unknown | the trace lacks a final answer step, or the data cannot support a call |

A tainted verdict is the finding the tool exists for: the pipeline looked
healthy at every step and the answer is still wrong.

## Repository layout

```
corruptchain/
  src/corruptchain/
    trace.py       strict trace parsing into ordered steps
    degraded.py    the degraded-source classes and their rules
    depends.py     dependency graph, declared and inferred edges
    taint.py       forward taint propagation with a reason chain
    verdict.py     grounded / tainted / unknown decision
    report.py      line-oriented deterministic rendering
    cli.py         subcommands and exit codes
  samples/         clean and contaminated trace fixtures
  tests/           suite per module and for the CLI
  scripts/verify.py  the eight check quality gate
  docs/assets/     logo and taint path diagram
```

## Why keep the reason chain

A verdict alone ("tainted") is not actionable. The reason chain names the
origin, the path, and whether each hop was declared or inferred, so the fix is
obvious: repair the empty tool call, or add the missing reference that would
have made the path declared in the first place.

## What it does not do

- It does not execute or repair anything. It reads a trace and reasons about
  the declared structure.
- It does not judge whether a degraded source was avoidable. It reports the
  class and the rule that produced it.
- It does not guess. A trace without a final answer step is `unknown`, not
  grounded.

## License

MIT. See `LICENSE`.

<!-- draft note 328 -->
