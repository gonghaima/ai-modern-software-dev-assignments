from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreateRequest, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreateRequest) -> NoteResponse:
    note_id = db.insert_note(payload.content)
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=500, detail="note not found after insert")
    return {
        "id": note["id"],
        "content": note["content"],
        "created_at": note["created_at"],
    }


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")
    return {"id": note["id"], "content": note["content"], "created_at": note["created_at"]}

