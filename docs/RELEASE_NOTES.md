# Release notes

## Prompt-template audit — 2026-10-13

- Relabeled the released checkpoint and historical results as
  `qwen-native-v0`.
- Added the versioned `simpletool-v2-vlm-v1` builder matching the original
  text-only SimpleTool v2 layout when no image is present, plus deterministic
  Qwen-VL image placeholders for multimodal rows.
- Removed the ambiguous `native`/`legacy` naming. The former `legacy` path was
  not the original SimpleTool v2 prompt because it still passed through the
  Qwen chat template.
- Historical checkpoints and metrics remain available, but they are not
  evidence for ICML SimpleTool v2 prompt compatibility.

- `corrected_mixed_frozen_r4`: Qwen3-VL-4B, Direct/Adaptive structured image tool calls.
- Dynamic head activation follows the largest property count in the supplied tool schemas.
- Raw branch output and legality are returned for auditability.
- BF16 is the reference checkpoint; quantized exports are separate artifacts.
