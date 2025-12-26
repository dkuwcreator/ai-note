"""Retry utilities with exponential backoff delays for AI calls."""
from __future__ import annotations
import time
from typing import Iterable, List

def backoff_delays(max_retries: int = 2, base_seconds: float = 0.5) -> List[float]:
    """Return a list of delays for retries.

    By spec: start at 0.5s then 1.5s for two retries (exponential-ish backoff).
    """
    if max_retries <= 0:
        return []
    delays: List[float] = []
    # Use a simple pattern: base, base * 3, base * 3^2, ... up to max_retries
    multiplier = 1
    for i in range(max_retries):
        delays.append(base_seconds * multiplier)
        multiplier *= 3
    return delays

def retry_loop(max_retries: int = 2, base_seconds: float = 0.5) -> Iterable[float]:
    """Yield delays between retries; caller should catch exceptions and sleep accordingly."""
    for d in backoff_delays(max_retries, base_seconds):
        yield d

def sleep_delays(max_retries: int = 2, base_seconds: float = 0.5) -> None:
    for d in retry_loop(max_retries, base_seconds):
        time.sleep(d)
