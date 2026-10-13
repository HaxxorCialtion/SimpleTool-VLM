import json
import unittest

from inference.prompting import VISION_PLACEHOLDER, build_simpletool_v2_vlm


class PromptingTest(unittest.TestCase):
    def setUp(self):
        self.system = "Route the command."
        self.query = "Amiya use skill now"
        self.tools = [{
            "type": "function",
            "function": {
                "name": "use_skill",
                "parameters": {"type": "object", "properties": {"unit_id": {"type": "string"}}},
            },
        }]

    def test_text_layout_matches_original_simpletool_v2(self):
        tool_text = json.dumps(self.tools[0], ensure_ascii=False, separators=(",", ":"))
        expected = (
            f"<|im_start|>system\n{self.system}\n\n## Available Tools:\n\n{tool_text}<|im_end|>\n"
            f"<|im_start|>user\nhistory: []\n\n{self.query}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        actual = build_simpletool_v2_vlm(
            [{"role": "system", "content": self.system}, {"role": "user", "content": self.query}],
            self.tools, history="[]")
        self.assertEqual(actual, expected)
        self.assertNotIn("<tool_call>", actual)

    def test_image_placeholder_is_deterministic(self):
        prompt = build_simpletool_v2_vlm(
            [{"role": "system", "content": self.system}, {"role": "user", "content": self.query}],
            self.tools, image_count=2, history="[]")
        self.assertEqual(prompt.count(VISION_PLACEHOLDER), 2)
        self.assertIn("history: []", prompt)


if __name__ == "__main__":
    unittest.main()
