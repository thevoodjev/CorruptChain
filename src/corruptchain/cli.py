"""corruptchain command line interface.

Subcommands:

    graph    TRACE    print the dependency graph, declared and inferred edges
    taint    TRACE    print degraded sources and the full taint path
    verdict  TRACE    judge whether the final answer is grounded, tainted, or
                      unknown. Exit 1 when the answer is tainted.
    version           print the version

