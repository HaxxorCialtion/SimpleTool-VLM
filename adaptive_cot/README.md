# SimpleTool-VLM-Adaptive

This is the Adaptive research track for SimpleTool-VLM. It emits a bounded
short `content` field before the function and dynamically active argument
heads. Empty content is valid; a non-empty field is a compact task rationale,
not a verbatim chain-of-thought claim.

## Current status

- The Direct path is the reproducible baseline.
- Adaptive checkpoints and training recipes are under active evaluation.
- Current distribution-shifted Classic evaluations do not establish a stable
  accuracy or latency gain over Direct.
- A stronger, better-controlled Adaptive model is **coming soon**.

## Reporting rule

Report content presence, schema legality, exact tool/argument accuracy, and
latency separately. Do not use the presence of `content` as evidence that the
model exposed private internal reasoning.

## Protocol

The `content` branch terminates at `</content>`. The function and each active
argument branch terminate independently. The runtime must preserve the raw
branches so a reviewer can distinguish an empty Adaptive response from a
transport or parsing failure.
