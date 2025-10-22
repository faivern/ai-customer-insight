# core/guards.py
# Input sanitization + prompt-injection guard rails.
#
# Goals:
#  - Limit per-sample length and total samples (cost & latency control).
#  - Strip control characters and null bytes.
#  - Neutralize typical injection patterns ("IGNORE ALL INSTRUCTIONS", "SYSTEM:", etc.).
#  - Detect suspicious content and emit warnings (transparency).
#  - Ensure we NEVER let samples override system instructions.

import re
from typing import List, Tuple

# Hard caps to reduce cost and mitigate malicious payloads / mega-prompts
MAX_SAMPLES = 200
MAX_CHARS_PER_SAMPLE = 800  # conservative per sample; tune as needed

# Simple suspicious patterns to warn about (extend if needed)
SUSPECT_PATTERNS = [
    r"(?i)\bignore all instructions\b",
    r"(?i)\boverride\b.*\binstructions\b",
    r"(?i)\bdisregard\b.*\brules\b",
    r"(?i)\bsystem:\b",           # attempts to masquerade as system role
    r"(?i)\bassistant:\b",        # attempts to masquerade as assistant role
    r"(?i)\buser:\b.*\bsystem\b", # "user: system do X"
    r"(?i)\b<<.*system.*>>",      # bracketed pseudo-system blocks
]

CONTROL_CHARS = re.compile(r"[\x00-\x08\x0B-\x1F\x7F]")

def _strip_control_chars(text: str) -> str:
    return CONTROL_CHARS.sub("", text)

def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + " …[truncated]"

def _neutralize_injection_markers(text: str) -> str:
    # Replace likely role markers that try to impersonate system/assistant
    text = re.sub(r"(?i)\bsystem:\b", "[role-redacted:system]", text)
    text = re.sub(r"(?i)\bassistant:\b", "[role-redacted:assistant]", text)
    text = re.sub(r"(?i)\buser:\b", "[role-redacted:user]", text)
    return text

def _detect_suspicious(text: str) -> List[str]:
    warnings = []
    for pat in SUSPECT_PATTERNS:
        if re.search(pat, text):
            warnings.append(f"Suspicious pattern matched: /{pat}/")
    return warnings

def sanitize_samples(samples: List[str]) -> Tuple[List[str], List[str]]:
    """
    Returns sanitized_samples, warnings.
    - Enforces caps
    - Strips control chars
    - Truncates long samples
    - Neutralizes role markers
    - Aggregates warnings for transparency
    """
    warnings: List[str] = []
    if len(samples) > MAX_SAMPLES:
        warnings.append(f"Sample count capped: {len(samples)} -> {MAX_SAMPLES}")

    clean: List[str] = []
    for i, s in enumerate(samples[:MAX_SAMPLES]):
        original = s
        s = _strip_control_chars(s)
        s = _truncate(s, MAX_CHARS_PER_SAMPLE)
        s = _neutralize_injection_markers(s)

        # collect warnings if suspicious
        ws = _detect_suspicious(original)
        warnings.extend(ws)

        clean.append(s)

    return clean, warnings

def guard_rails_summary(warnings: List[str]) -> str:
    if not warnings:
        return "Guard rails: OK (no suspicious patterns detected)."
    # Keep it short for the report footer
    uniq = list(dict.fromkeys(warnings))  # de-dup while preserving order
    trimmed = uniq[:8]
    more = f" (+{len(uniq)-8} more)" if len(uniq) > 8 else ""
    return "Guard rails warnings: " + "; ".join(trimmed) + more
