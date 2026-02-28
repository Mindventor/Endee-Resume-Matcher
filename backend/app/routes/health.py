"""Health check route."""

from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services import endee_service
from app.config import settings

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API and Endee connectivity status."""
    endee_ok = endee_service.check_connection()
    return HealthResponse(
        status="healthy" if endee_ok else "degraded",
        endee_connected=endee_ok,
        embedding_model=settings.embedding_model,
    )
