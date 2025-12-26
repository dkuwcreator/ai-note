"""Rewrite presets for AI assistant."""
from __future__ import annotations
from typing import Dict

PRESETS: Dict[str, str] = {
    "rewrite_clearer": "Rewrite the following text to be clearer and more concise:\n\n{input}",
    "shorten": "Shorten the following text while preserving meaning:\n\n{input}",
    "make_more_formal": "Make the following text more formal:\n\n{input}",
    "fix_grammar": "Fix grammar and spelling in the following text:\n\n{input}",
    "bullet_points": "Convert the following text into bullet points:\n\n{input}",
}

def build_prompt(preset_key: str, input_text: str) -> str:
    template = PRESETS.get(preset_key)
    if not template:
        raise KeyError(f"Unknown preset {preset_key}")
    return template.format(input=input_text)
