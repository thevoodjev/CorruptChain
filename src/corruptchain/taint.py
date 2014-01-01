"""Forward taint propagation with a reason chain.

Taint originates at degraded sources (degraded.py) and flows forward along
dependency edges (depends.py). A step is tainted when it depends, directly or
transitively, on at least one degraded source. Every tainted step records the
chain of reasons that reached it, so the full path from the silent hole to the
final answer can be printed.

The reason chain is honest about edge strength. Each hop stores whether the
edge that carried the taint was declared or inferred, because a taint path that
runs entirely through declared edges is stronger evidence of contamination than
one that leans on an inferred value match.

