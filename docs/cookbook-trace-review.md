# Cookbook: reviewing a trace

```
python -m corruptchain verdict trace.json
```

Start with the verdict, then read `taint` for the origin and the path. A
tainted verdict with an inferred hop is worth a second look at the step that
introduced the missing reference.
