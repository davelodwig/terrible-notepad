from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)
from app.routers.notes import router as notes_router
from app.routers.health import router as health_router
from app import apm
from app import db


@app.on_event("startup")
async def startup_event():
    # initialize DB and APM using centralized settings
    if settings.mongo_uri:
        # set env expected variables for legacy code paths
        import os

        os.environ.setdefault("MONGO_URI", settings.mongo_uri)
        os.environ.setdefault("MONGO_DB", settings.mongo_db)
    await db.init_app(app)
    apm.init_app(app)


app.include_router(health_router)
app.include_router(notes_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
