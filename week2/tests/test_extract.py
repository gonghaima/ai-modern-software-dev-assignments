import pytest

from ..app.services import extract as extract_module
from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def _fake_chat_response(payload: str):
    class _Msg:
        def __init__(self, content: str) -> None:
            self.content = content

    class _Resp:
        def __init__(self, content: str) -> None:
            self.message = _Msg(content)

    return _Resp(payload)


def test_extract_action_items_llm_bullets(monkeypatch):
    payload = '{"action_items": ["Set up database", "Write tests"]}'

    def _fake_chat(*_args, **_kwargs):
        return _fake_chat_response(payload)

    monkeypatch.setattr(extract_module, "chat", _fake_chat)

    text = "- [ ] Set up database\n- Write tests"
    items = extract_action_items_llm(text)
    assert items == ["Set up database", "Write tests"]


def test_extract_action_items_llm_keyword_prefixed(monkeypatch):
    payload = '{"action_items": ["Email client", "Schedule meeting"]}'

    def _fake_chat(*_args, **_kwargs):
        return _fake_chat_response(payload)

    monkeypatch.setattr(extract_module, "chat", _fake_chat)

    text = "todo: email client\naction: schedule meeting"
    items = extract_action_items_llm(text)
    assert items == ["Email client", "Schedule meeting"]


def test_extract_action_items_llm_empty_input(monkeypatch):
    payload = '{"action_items": []}'

    def _fake_chat(*_args, **_kwargs):
        return _fake_chat_response(payload)

    monkeypatch.setattr(extract_module, "chat", _fake_chat)

    text = "   "
    items = extract_action_items_llm(text)
    assert items == []


def test_extract_action_items_llm_fallback_on_bad_json(monkeypatch):
    def _fake_chat(*_args, **_kwargs):
        return _fake_chat_response("not-json")

    monkeypatch.setattr(extract_module, "chat", _fake_chat)

    text = "- [ ] Set up database"
    items = extract_action_items_llm(text)
    assert items == ["Set up database"]
