"""Build the data dependency graph of an agent run.

An edge from step A to step B means B consumed A's output. Edges are found two
ways, and the two are never treated as equal:

    declared   B listed A in its references field. This is the agent stating
               outright that it used A. Strong evidence.

    inferred   B did not list A, but A's output value appears verbatim inside
               B's output. We infer that B carried A's data forward. Weaker
               evidence, because a value can coincide, so it is labelled as an
               inference and never silently promoted to a declared fact.

The honesty rule from the brief lives here: every edge records how it was
established, and a report can list exactly which edges were inferred. When both
a declaration and a value match exist for the same pair, the edge is declared,
because the stronger evidence wins, and the value match is redundant.

