# SimpleTool-VLM

SimpleTool-VLM is a research release of a Qwen3-VL-4B model adapted for structured tool calls from images and text. It emits a function name and only the argument heads required by the supplied tool schema. The public release contains inference code and reproducibility notes; model weights are hosted separately on Hugging Face.

## Highlights

- Direct and Adaptive modes.
- Function plus dynamically sized `arg1...argN` heads (`N` is the maximum property count in the supplied tools).
- Image input is passed as pixels; invoice values are not copied into hidden prompt fields.
- Raw branch outputs and legality are preserved for auditing.

## Intended use

Research on real-time multimodal structured decisions, tool calling, and embodied-agent interfaces. This is not an OCR benchmark or a general invoice accounting system. Validate every action before execution.

## Model variants

- BF16 merged checkpoint: `Cialtion/SimpleTool-VLM`.
- W4A16 checkpoint: `Cialtion/SimpleTool-VLM-W4A16` (when the upload is complete).
- FP8 checkpoint: `Cialtion/SimpleTool-VLM-FP8` (when the upload is complete).

The quantized variants use the same task adapter and tokenizer contract; backend support depends on the serving stack.

## Quick start

The lightweight HTTP implementation is in `inference/`. It accepts one PNG, text messages, and OpenAI-style function tools. See `examples/invoice_request.json`. The service returns `prediction.raw`, `prediction.legal`, `events`, and server timings.

## Limitations

This release does not claim strict adapter-to-merged numerical parity, arbitrary-image robustness, OCR superiority, or native Qwen chain-of-thought. Adaptive `content` is a short task-controlled field. The included invoice demo is an end-to-end protocol demonstration, not a financial approval system.

## License and attribution

Code and release documentation are Apache-2.0. The checkpoint remains subject to the Qwen3-VL base-model license and any upstream terms. Users must review upstream terms before redistribution or commercial deployment.
