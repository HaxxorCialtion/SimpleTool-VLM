# Canonical SimpleTool v2 VLM retraining contract

Preserve old checkpoints and metrics as `qwen-native-v0`. New training must
import `inference/prompting.py` and select `simpletool-v2-vlm-v1`; it must not
call `apply_chat_template` in the canonical prompt path.

Every run manifest must record the prompt-template ID, prompt-builder source
hash, rendered prompt SHA256, image SHA256, and special-token IDs. Two-card and
four-card experiments must share the same frozen prompt builder and dataset
manifest.

Before GPU training, render and retain text-only, single-image, and multi-turn
samples. The text-only sample must be byte-identical to the original
`SimpleTool/01_benchmark.py::build_prompt(..., "v2")` layout. Canonical prompts
must fail validation if they contain `<tool_call>`, `<tools>`, or `# Tools`.

Evaluate the old and new checkpoints in a 2×2 checkpoint/template matrix, but
report the old-native/new-v2 matched cells separately. Cross-template cells
are mismatch diagnostics, not benchmark results. A new service is accepted
only when model metadata reports `prompt_template: simpletool-v2-vlm-v1`.
