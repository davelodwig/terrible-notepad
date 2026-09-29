import os
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document


class NoteDocument(Document):
    title: str
    content: Optional[str] = None

    class Settings:
        name = "notes"


class BeanieStore:
    async def create(self, title: str, content: Optional[str] = None) -> Dict[str, Any]:
        doc = NoteDocument(title=title, content=content)
        await doc.insert()
        return {"id": str(doc.id), "title": doc.title, "content": doc.content}

    async def update(self, note_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        doc = await NoteDocument.get(note_id)
        if not doc:
            return None
        for k, v in data.items():
            if v is not None:
                setattr(doc, k, v)
        await doc.save()
        return {"id": str(doc.id), "title": doc.title, "content": doc.content}

    async def delete(self, note_id: str) -> bool:
        doc = await NoteDocument.get(note_id)
        if not doc:
            return False
        await doc.delete()
        return True


async def init_app(app: FastAPI) -> None:
    """Initialize Mongo/Beanie store. If `MONGO_URI` is not set, this becomes a no-op.

    Attaches a `store` object to `app.state` with async methods: `create`, `update`, `delete`.
    """
    uri = os.getenv("MONGO_URI")
    dbname = os.getenv("MONGO_DB", "terrible")
    if not uri:
        # DB not configured; leave app without a store. Endpoints will return 503.
        return

    client = AsyncIOMotorClient(uri)
    await init_beanie(database=client[dbname], document_models=[NoteDocument])
    app.state.store = BeanieStore()


def get_store(request: Request) -> BeanieStore:
    store = getattr(request.app.state, "store", None)
    if store is None:
        raise HTTPException(status_code=503, detail="Database not configured")
    return store
