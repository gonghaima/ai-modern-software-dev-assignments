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
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> TODO 

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
>TODO 



