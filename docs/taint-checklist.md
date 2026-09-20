# Taint checklist

- Does every tool step declare a status, and is `empty` handled by consumers?
- Do declared references cover every value that appears verbatim downstream?
- Does the final answer step exist and reference at least one grounded source?
- Are inferred hops treated as weaker evidence in the review?
