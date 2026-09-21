# Multi-tool decision training

This document describes the optional Jev-like ranking mode. It is separate
from the invoice Direct/Adaptive release.

The host fixes an ordered candidate list, for example:

```python
candidates = ("record_expense", "ask_expert", "reject", "defer")
```

The model emits one `multi_tool` function and `arg1..argK`, where K is the
number of candidates. `arg1` maps to the first candidate, and so on. Each
value is a bounded ranking score. The host selects the maximum score, with the
first candidate winning a tie. Scores are not calibrated probabilities: do
not normalize them or require their sum to equal one.

Training data should cover K in 2, 3, 4, and 6; randomize candidate order;
include text and genuine image inputs; and preserve the candidate identity in
the audit metadata. A simple target is 0.9 for the winner and 0.1 for the
others, with additional 0.8/0.2 and 0.6/0.4 margins. The objective is ranking,
not probability calibration. The prompt must not copy numeric image content.

Start with Direct-only rows. Add Adaptive rows after Direct has stable
candidate-identity accuracy. Runtime generation must activate only the K
needed argument heads.

Report argmax accuracy, candidate-identity accuracy after permutation,
schema legality, out-of-range scores, latency by K and modality, and the
legacy invoice regression. This mode is Jev-like at the interface level; it is
not a claim of Jev's architecture or benchmark results.
