# Week 7 – Implementation Plan

## Task 1: Add more endpoints and validations

**Missing endpoints:**
- `GET /action-items/{item_id}` — no single-item fetch exists
- `DELETE /notes/{note_id}` — no delete endpoint exists
- `DELETE /action-items/{item_id}` — no delete endpoint exists

**Missing validations:**
- `NoteCreate.title` and `NoteCreate.content` have no min-length constraint
- `ActionItemCreate.description` has no min-length constraint

**Steps:**
1. Add `min_length=1` to `NoteCreate.title`, `NoteCreate.content`, `ActionItemCreate.description` in `schemas.py`
2. Add `DELETE /notes/{note_id}` (204) to `routers/notes.py`
3. Add `GET /action-items/{item_id}` and `DELETE /action-items/{item_id}` (204) to `routers/action_items.py`
4. Add tests for new endpoints and validation errors (422 on empty strings)

---

## Task 2: Extend extraction logic

**Current state:** `extract_action_items` only catches `TODO:`, `ACTION:` prefixes and `!`-ending lines.

**Steps:**
1. Add patterns:
   - Prefixes: `FIXME:`, `FOLLOW-UP:`, `FOLLOW UP:`
   - Lines containing action phrases: "need to", "must", "should", "please" (case-insensitive)
2. Strip leading bullet/dash/number markers before matching
3. Add tests in `test_extract.py` covering all new patterns

---

## Task 3: Add a new model and relationships

**Current state:** `Note` and `ActionItem` are unrelated models.

**Steps:**
1. Add `note_id = Column(Integer, ForeignKey("notes.id"), nullable=True)` to `ActionItem`; add `relationship` on `Note` → `action_items` in `models.py`
2. Add `note_id: int | None` to `ActionItemCreate` and `ActionItemRead` in `schemas.py`
3. Add `POST /notes/{note_id}/action-items` to create an action item linked to a note
4. Add `GET /notes/{note_id}/action-items` to list action items for a note
5. Add tests for the new relationship endpoints

---

## Task 4: Improve tests for pagination and sorting

**Current state:** Tests only do a single basic pagination/sort check with no order or boundary verification.

**Steps — add tests in `test_notes.py` and `test_action_items.py` for:**
1. `skip` + `limit`: create N items, verify `skip=1&limit=2` returns exactly 2 items starting from the second
2. Ascending vs descending sort: verify returned ids are in correct order for `sort=created_at` vs `sort=-created_at`
3. `limit=1` boundary: verify exactly 1 item is returned
4. Invalid `sort` field: verify no 500 (falls back gracefully)
5. `completed=false` filter: verify only incomplete action items are returned
