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
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

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



