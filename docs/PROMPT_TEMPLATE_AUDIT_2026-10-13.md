# Prompt-template audit — 2026-10-13

## Finding

The released `corrected_mixed_frozen_r4` checkpoint, its FP8 export, and the
historical VLM evaluation path used the Qwen3-VL native tool template via:

```python
processor.apply_chat_template(
    messages,
    tools=tools,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False,
)
```

That template renders `# Tools`, `<tools>`, and `<tool_call>` instructions. It
is not the prompt used by the original ICML SimpleTool v2 implementation.

The original text-only v2 layout in `SimpleTool/01_benchmark.py` is:

```text
<|im_start|>system
{system}

## Available Tools:

{one compact JSON tool per line}<|im_end|>
<|im_start|>user
history: {history}

{query}<|im_end|>
<|im_start|>assistant
```

The previously published `legacy` option was also not equivalent: it appended
`# Available Tools` to a system message and then still passed the result
through the Qwen chat template.

## Impact

- The old checkpoint remains a valid native-template VLM experiment.
- Its historical metrics describe `qwen-native-v0`, not ICML SimpleTool v2.
- The old results cannot establish prompt compatibility with the text-only
  ICML model or be used as a fixed-template comparison.
- Changing the inference prompt does not repair a checkpoint trained on the
  other template; retraining or an explicitly controlled adaptation is needed.

## Remediation

- Preserve old checkpoints and results, labeled `qwen-native-v0`.
- Add the versioned `simpletool-v2-vlm-v1` builder.
- Require the serving process to report its prompt-template identity.
- Verify that the text-only layout is byte-for-byte identical to
  `build_prompt(..., "v2")` for the same compact JSONL tools.
- Insert deterministic Qwen-VL image placeholders only for multimodal rows.
- Train and evaluate new checkpoints on the same frozen builder; do not mix
  old and new template metrics.

## Verification performed

- Unit tests confirm exact text-only v2 layout and absence of `<tool_call>`.
- A real Qwen3-VL processor encoded the new image placeholder path and returned
  both `pixel_values` and `input_ids`.
- The native processor output was captured and confirmed to contain the Qwen
  `<tools>` / `<tool_call>` instructions.
