from __future__ import annotations

import re
from typing import List
import json
from ollama import chat
from dotenv import load_dotenv
import logging

from ..config import OLLAMA_MODEL

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    return _extract_with_regex(text)


def _extract_with_regex(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> List[str]:
    try:
        response = chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that extracts action items from text. Return ONLY a JSON object with an 'action_items' key containing an array of strings. Each string should be one action item. Example: {\"action_items\": [\"Update database\", \"Review code\"]}"
                },
                {
                    "role": "user",
                    "content": f"Extract all action items from the following text:\n\n{text}"
                }
            ],
            format="json"
        )

        result = json.loads(response.message.content)

        # Handle different response formats
        if isinstance(result, dict) and "action_items" in result:
            items = result["action_items"]
        elif isinstance(result, list):
            items = result
        else:
            items = []

        return [str(item).strip() for item in items if str(item).strip()]
    except Exception:
        logging.exception("LLM extraction failed")
        # Fallback to regex if LLM fails
        return _extract_with_regex(text)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
