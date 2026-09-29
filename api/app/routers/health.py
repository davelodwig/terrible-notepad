from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", include_in_schema=True)
def health():
    """Health endpoint returning service status."""
    return {"status": "ok"}
