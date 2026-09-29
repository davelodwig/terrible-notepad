from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.db import get_store

router = APIRouter(prefix="/notes", tags=["notes"])


class Note(BaseModel):
    id: str
    title: str
    content: Optional[str] = None


class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate, request: Request):
    store = get_store(request)
    note = await store.create(payload.title, payload.content)
    return note


@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, payload: NoteUpdate, request: Request):
    store = get_store(request)
    update_data: Dict[str, Any] = payload.dict(exclude_unset=True)
    updated = await store.update(note_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, request: Request):
    store = get_store(request)
    ok = await store.delete(note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
