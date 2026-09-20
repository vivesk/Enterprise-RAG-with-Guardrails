import re


# Lightweight baseline rules. Production systems should combine
# deterministic rules with a classifier/policy engine and tool authorization.
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(the\s+)?system\s+prompt",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+hidden\s+instructions",
    r"developer\s+message",
    r"jailbreak",
    r"disable\s+your\s+safety",
]


def detect_prompt_injection(text: str) -> tuple[bool, str]:
    """Return (blocked, reason) for obvious prompt-injection attempts."""
    normalized = " ".join(text.lower().split())

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, normalized):
            return True, f"Potential prompt injection detected: {pattern}"

    return False, ""
