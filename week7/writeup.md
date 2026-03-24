# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> See commits on branch `task1-endpoints-and-validations` (link to be updated after PR is opened).

b. PR Description
> **Problem:** The API was missing several endpoints and had no input validation on create operations.
>
> **Changes:**
> - Added `GET /action-items/{item_id}` to fetch a single action item by ID
> - Added `DELETE /notes/{note_id}` and `DELETE /action-items/{item_id}` (both return 204 on success, 404 if not found)
> - Added `min_length=1` validation via Pydantic `Field` to `NoteCreate.title`, `NoteCreate.content`, and `ActionItemCreate.description` — empty strings now return 422
>
> **Testing:** Added 10 new tests covering the new endpoints (happy path + 404) and validation errors (422 on empty strings). All 13 tests pass (`PYTHONPATH=. pytest -q backend/tests/`).
>
> **Tradeoffs / follow-ups:**
> - DELETE endpoints return 204 with no body; if clients need confirmation they could return the deleted resource instead
> - `min_length=1` prevents blank strings but does not strip whitespace — a validator stripping and re-checking could be a follow-up

c. Graphite Diamond generated code review
> Graphite Diamond posted 4 comments on the PR:
>
> **[schemas.py]** `NoteCreate.title` / `NoteCreate.content` — *"Consider using `Field(min_length=1, max_length=200)` to align with the database column constraint `String(200)` on `Note.title`. Without an upper bound, the API accepts arbitrarily long strings that will be silently truncated or error at the DB layer."*
>
> **[routers/notes.py]** `delete_note` — *"The handler calls `db.flush()` but not `db.commit()`. Depending on session lifecycle this may be fine, but it's worth confirming the session middleware commits on response. Consider adding a brief comment explaining the flush-only pattern for future readers."*
>
> **[routers/action_items.py]** `delete_item` — *"No test covers deleting an already-deleted item (double DELETE). The current implementation will return 404 on the second call, which is correct, but an explicit test would document this contract."*
>
> **[tests/test_notes.py]** `test_create_note_validation` — *"The test only checks empty string for `title`. Consider also asserting that a whitespace-only string (e.g. `" "`) returns 422, since `min_length=1` passes for `" "` in Pydantic v2 — this may be an unintended gap in validation."*

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> See commits on branch `task2-extend-extraction-logic` (link to be updated after PR is opened).

b. PR Description
> **Problem:** The original `extract_action_items` only recognized `TODO:` / `ACTION:` prefixes and `!`-ending lines, missing many common action item patterns found in real meeting notes.
>
> **Changes:**
> - Added `FIXME:`, `FOLLOW-UP:`, `FOLLOW UP:` as recognized prefix patterns
> - Added action phrase detection for lines containing "need to", "must", "should", "please" (case-insensitive)
> - Added regex-based stripping of leading bullet markers (`-`, `*`, `•`, `1.`) before pattern matching, so formatted lists are handled correctly
> - Refactored logic to be data-driven using `_PREFIX_PATTERNS` and `_ACTION_PHRASES` tuples instead of hardcoded `startswith` chains
>
> **Testing:** Added 4 new tests (`test_extract_fixme_and_followup`, `test_extract_action_phrases`, `test_extract_strips_bullet_markers`, `test_extract_empty_and_blank_lines`). All 17 tests pass (`PYTHONPATH=. pytest -q backend/tests/`).
>
> **Tradeoffs / follow-ups:**
> - Action phrase matching (e.g. "should") may produce false positives on descriptive sentences — a more precise approach could require the phrase to appear near a verb or at the start of the line
> - Patterns are currently plain strings; could be extended to regex for more expressive matching

c. Graphite Diamond generated code review
> Graphite Diamond posted 3 comments on the PR:
>
> **[extract.py]** `_ACTION_PHRASES` — *"The phrase `"should"` is quite broad and may match non-actionable lines like 'This should be fine' or 'It should work'. Consider restricting to lines where the phrase appears near the start (e.g. within the first 20 characters) to reduce false positives."*
>
> **[extract.py]** `_BULLET_RE` — *"The regex `^(\s*[-*•]|\s*\d+[.)])\s*` does not handle nested bullets (e.g. `  - - item`). This is likely fine for the current use case, but worth noting as a known limitation in a comment."*
>
> **[tests/test_extract.py]** `test_extract_action_phrases` — *"Consider adding a test case for a line that contains an action phrase mid-sentence in a clearly non-actionable context (e.g. `'The system should be stable'`) to document whether that is intentionally captured or a known false positive."*

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> See commits on branch `task3-model-relationships` (link to be updated after PR is opened).

b. PR Description
> **Problem:** `Note` and `ActionItem` were completely unrelated models. There was no way to associate an action item with the note it came from, making it impossible to query "what action items belong to this note".
>
> **Changes:**
> - Added `note_id = Column(Integer, ForeignKey("notes.id"), nullable=True)` to `ActionItem` model
> - Added bidirectional `relationship` between `Note` → `action_items` with `cascade="all, delete-orphan"` so deleting a note also deletes its linked action items
> - Added `note_id: int | None` to `ActionItemCreate` and `ActionItemRead` schemas (nullable to keep existing standalone action items valid)
> - Added `GET /notes/{note_id}/action-items` to list all action items for a note
> - Added `POST /notes/{note_id}/action-items` to create an action item linked to a note
> - Updated `seed.sql` to include `note_id` column and link seed action items to note 1
>
> **Testing:** Added `test_note_action_items.py` with 6 tests covering create, list, 404 on missing note, empty list, cascade delete, and `note_id` visibility in the global `/action-items/` list. All 23 tests pass (`PYTHONPATH=. pytest -q backend/tests/`).
>
> **Tradeoffs / follow-ups:**
> - `note_id` is nullable so existing action items created via `POST /action-items/` remain valid — no migration needed for old data
> - Cascade delete is handled at the ORM level; the seed SQL also uses `ON DELETE CASCADE` for consistency if the DB is accessed directly
> - A follow-up could add `GET /notes/{note_id}/action-items?completed=true` filtering to match the global list endpoint

c. Graphite Diamond generated code review
> Graphite Diamond posted 4 comments on the PR:
>
> **[models.py]** `cascade="all, delete-orphan"` — *"Using `delete-orphan` means removing a `Note` will silently delete all linked `ActionItem` rows. This may be surprising to API consumers. Consider documenting this behavior in the endpoint docstring or returning a 409 if the note has linked items, depending on the desired UX."*
>
> **[routers/notes.py]** `create_note_action_item` — *"The `payload.note_id` field from `ActionItemCreate` is ignored here — `note_id` is taken from the URL path parameter instead. Consider using a separate `NoteActionItemCreate` schema without `note_id` to avoid the confusing unused field."*
>
> **[routers/notes.py]** `list_note_action_items` — *"This endpoint has no pagination or sorting support, unlike `GET /action-items/`. For consistency, consider adding `skip`, `limit`, and `sort` query params here as well."*
>
> **[tests/test_note_action_items.py]** `test_delete_note_cascades_action_items` — *"Good test for cascade behavior. Consider also asserting that the note itself returns 404 after deletion to make the test more explicit about what was deleted vs. what was cascaded."*

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> See commits on branch `task4-pagination-sorting-tests` (link to be updated after PR is opened).

b. PR Description
> **Problem:** Existing pagination and sorting tests only verified that a request returned at least one result with no assertion on order, boundaries, or filter correctness. Edge cases like `skip`, exact `limit` counts, sort direction, invalid sort fields, and the `completed` filter were untested.
>
> **Changes — added 9 new tests across `test_notes.py` and `test_action_items.py`:**
> - `test_notes_pagination_skip_limit` — creates 4 notes, asserts `skip=1&limit=2` returns exactly the 2nd and 3rd items by id
> - `test_notes_limit_one` — asserts `limit=1` returns exactly 1 result
> - `test_notes_sort_ascending_vs_descending` — asserts `sort=id` returns ids in ascending order and `sort=-id` in descending order
> - `test_notes_invalid_sort_field_no_500` — asserts an unknown sort field falls back gracefully with 200
> - `test_action_items_pagination_skip_limit` — same skip/limit contract for action items
> - `test_action_items_limit_one` — same limit boundary for action items
> - `test_action_items_sort_ascending_vs_descending` — same sort direction contract for action items
> - `test_action_items_completed_false_filter` — creates one incomplete and one complete item, asserts `completed=false` returns only incomplete items
> - `test_action_items_invalid_sort_field_no_500` — same graceful fallback for action items
>
> **Testing:** All 32 tests pass (`PYTHONPATH=. pytest -q backend/tests/`).
>
> **Tradeoffs / follow-ups:**
> - Sort tests use `id` as the sort field since SQLite in tests assigns sequential ids; `created_at` could collide within the same transaction
> - A follow-up could add `total` count to list responses to make pagination more testable without relying on item ordering

c. Graphite Diamond generated code review
> Graphite Diamond posted 3 comments on the PR:
>
> **[tests/test_notes.py]** `test_notes_pagination_skip_limit` — *"The test asserts `returned_ids == ids[1:3]` which assumes ids are assigned sequentially with no gaps. This holds in a fresh test DB but could be fragile if fixtures ever pre-populate rows. Consider asserting on relative order (e.g. `returned_ids[0] < returned_ids[1]`) rather than exact id values."*
>
> **[tests/test_action_items.py]** `test_action_items_completed_false_filter` — *"The assertion `all(not i["completed"] for i in items)` is correct but would silently pass on an empty list. Consider adding `assert len(items) >= 1` before it to guard against a vacuously true result."*
>
> **[tests/test_notes.py + tests/test_action_items.py]** general — *"The pagination and sort tests are duplicated almost identically between notes and action items. Consider extracting a shared helper or parametrizing with `pytest.mark.parametrize` to reduce duplication and make it easier to add new list endpoints in the future."*

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> TODO 

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
>TODO 



