from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class NoteCreateRequest(BaseModel):
    content: str = Field(min_length=1)

    @field_validator("content")
    @classmethod
    def strip_content(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("content must not be empty")
        return stripped


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ExtractRequest(BaseModel):
    text: str = Field(min_length=1)
    save_note: bool = False

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("text must not be empty")
        return stripped


class ExtractItemResponse(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ExtractItemResponse]


class ActionItemResponse(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


class MarkDoneRequest(BaseModel):
    done: bool = True


class MarkDoneResponse(BaseModel):
    id: int
    done: bool
