from app.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/health")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "is_healthy?": "Oui",
        "environment": settings.environment,
        "testing": settings.testing,
    }

