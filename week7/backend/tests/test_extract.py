from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_fixme_and_followup():
    items = extract_action_items(
        "FIXME: handle edge case\nFOLLOW-UP: check with team\nFOLLOW UP: update docs"
    )
    assert "FIXME: handle edge case" in items
    assert "FOLLOW-UP: check with team" in items
    assert "FOLLOW UP: update docs" in items


def test_extract_action_phrases():
    items = extract_action_items(
        "We need to deploy by Friday\nYou must update the config\nPlease review this\nWe should refactor later\nThis is fine"
    )
    assert "We need to deploy by Friday" in items
    assert "You must update the config" in items
    assert "Please review this" in items
    assert "We should refactor later" in items
    assert "This is fine" not in items


def test_extract_strips_bullet_markers():
    items = extract_action_items(
        "- TODO: with dash\n* FIXME: with asterisk\n1. ACTION: numbered\n• TODO: with bullet"
    )
    assert "TODO: with dash" in items
    assert "FIXME: with asterisk" in items
    assert "ACTION: numbered" in items
    assert "TODO: with bullet" in items


def test_extract_empty_and_blank_lines():
    assert extract_action_items("") == []
    assert extract_action_items("   \n\n   ") == []


