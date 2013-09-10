"""Build the data dependency graph of an agent run.

An edge from step A to step B means B consumed A's output. Edges are found two
ways, and the two are never treated as equal:

    declared   B listed A in its references field. This is the agent stating
               outright that it used A. Strong evidence.

    inferred   B did not list A, but A's output value appears verbatim inside
               B's output. We infer that B carried A's data forward. Weaker
