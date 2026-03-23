import re

_PREFIX_PATTERNS = ("todo:", "action:", "fixme:", "follow-up:", "follow up:")
_ACTION_PHRASES = ("need to", "must", "should", "please")
_BULLET_RE = re.compile(r"^(\s*[-*•]|\s*\d+[.)])\s*")


def extract_action_items(text: str) -> list[str]:
    results: list[str] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        line = _BULLET_RE.sub("", raw).strip()
        normalized = line.lower()
        if any(normalized.startswith(p) for p in _PREFIX_PATTERNS):
            results.append(line)
        elif line.endswith("!"):
            results.append(line)
        elif any(phrase in normalized for phrase in _ACTION_PHRASES):
            results.append(line)
    return results
