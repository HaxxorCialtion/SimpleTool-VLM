"""Versioned prompt builders for SimpleTool-VLM.

``qwen-native-v0`` is the template used by the currently released checkpoint.
``simpletool-v2-vlm-v1`` is the deterministic multimodal extension of the
original ICML SimpleTool v2 prompt.  They are intentionally distinct: results
from one template must not be reported as results from the other.
"""
import json


QWEN_NATIVE_V0 = "qwen-native-v0"
SIMPLETOOL_V2_VLM_V1 = "simpletool-v2-vlm-v1"
PROMPT_TEMPLATES = (QWEN_NATIVE_V0, SIMPLETOOL_V2_VLM_V1)
VISION_PLACEHOLDER = "<|vision_start|><|image_pad|><|vision_end|>"


def _text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if not isinstance(part, dict):
                raise ValueError("message content parts must be objects")
            if part.get("type") == "text":
                value = part.get("text")
                if not isinstance(value, str):
                    raise ValueError("text part requires string text")
                parts.append(value)
            elif part.get("type") not in ("image", "image_url"):
                raise ValueError("unsupported message content part")
        return "\n".join(parts)
    raise ValueError("message content must be text or typed parts")


def _simpletool_fields(messages, explicit_history=None):
    systems = [_text(m.get("content")) for m in messages if m.get("role") == "system"]
    user_indices = [i for i, m in enumerate(messages) if m.get("role") == "user"]
    if not user_indices:
        raise ValueError("SimpleTool v2 requires a user message")
    last_user = user_indices[-1]
    query = _text(messages[last_user].get("content"))
    if explicit_history is None:
        previous = [
            {"role": m.get("role"), "content": _text(m.get("content"))}
            for i, m in enumerate(messages[:last_user]) if m.get("role") != "system"
        ]
        history = json.dumps(previous, ensure_ascii=False, separators=(",", ":"))
    elif isinstance(explicit_history, str):
        history = explicit_history
    else:
        history = json.dumps(explicit_history, ensure_ascii=False, separators=(",", ":"))
    return "\n\n".join(systems), history, query


def build_simpletool_v2_vlm(messages, tools, *, image_count=0, history=None):
    """Build the ICML v2 layout plus deterministic Qwen-VL image placeholders.

    When ``image_count`` is zero and ``history`` is supplied, this is byte-for-
    byte the layout produced by ``SimpleTool/01_benchmark.py::build_prompt`` for
    v2, assuming the same compact JSONL tool serialization.
    """
    if not isinstance(image_count, int) or image_count < 0:
        raise ValueError("image_count must be a nonnegative integer")
    system, history_text, query = _simpletool_fields(messages, history)
    tool_text = "\n".join(json.dumps(t, ensure_ascii=False, separators=(",", ":")) for t in tools)
    vision = "\n".join([VISION_PLACEHOLDER] * image_count)
    if vision:
        query = vision + ("\n" + query if query else "")
    return (
        f"<|im_start|>system\n{system}\n\n## Available Tools:\n\n{tool_text}<|im_end|>\n"
        f"<|im_start|>user\nhistory: {history_text}\n\n{query}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )


def build_prompt(processor, messages, tools, template, *, image_count=0, history=None):
    if template == QWEN_NATIVE_V0:
        return processor.apply_chat_template(
            messages, tools=tools, tokenize=False,
            add_generation_prompt=True, enable_thinking=False)
    if template == SIMPLETOOL_V2_VLM_V1:
        return build_simpletool_v2_vlm(
            messages, tools, image_count=image_count, history=history)
    raise ValueError("unknown prompt template: " + str(template))
