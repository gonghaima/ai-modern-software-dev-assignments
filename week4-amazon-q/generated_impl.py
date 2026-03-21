```python
@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, updated_note: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.content = updated_note.content
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)
```