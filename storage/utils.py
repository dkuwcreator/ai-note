"""Utility helpers for storage module."""
from __future__ import annotations
import re
from typing import List

_whitespace_re = re.compile(r"\s+")

def normalize_tag(name: str) -> str:
    s = name.strip()
    s = _whitespace_re.sub(' ', s)
    return s.lower()

def normalize_tags(names: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for n in names:
        nn = normalize_tag(n)
        if nn and nn not in seen:
            seen.add(nn)
            out.append(nn)
    return out
