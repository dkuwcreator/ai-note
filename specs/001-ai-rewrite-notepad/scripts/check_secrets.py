#!/usr/bin/env python3
"""
Simple repo scan for forbidden OpenAI public endpoints and literal API key patterns.
Intended as a lightweight diagnostic; CI should run a stricter scanner.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FORBIDDEN_PATTERNS = [
    re.compile(r"api\.openai\.com", re.I),
    re.compile(r"sk-[A-Za-z0-9-_]{30,}")  # naive key pattern
]


def scan():
    findings = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".md", ".env", ".txt", ".json", ".yaml", ".yml"}:
            try:
                text = p.read_text(encoding="utf8", errors="ignore")
            except Exception:
                continue
            for pat in FORBIDDEN_PATTERNS:
                if pat.search(text):
                    findings.append((str(p.relative_to(ROOT)), pat.pattern))
    return findings


if __name__ == "__main__":
    f = scan()
    if not f:
        print("No forbidden endpoints or key-like patterns found.")
    else:
        print("Potential secrets or forbidden endpoints found:")
        for path, pattern in f:
            print(f" - {path}: matches {pattern}")
        raise SystemExit(2)
