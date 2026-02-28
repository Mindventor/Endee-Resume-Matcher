"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import resume, analysis, health
from app.services import endee_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-30s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("=" * 60)
    logger.info(f"  {settings.app_name}")
    logger.info("  Powered by Endee Vector Database")
    logger.info("=" * 60)

    # Initialize Endee indexes
    connected = endee_service.ensure_indexes()
    if connected:
        logger.info("✓ Endee connected — all indexes ready")
    else:
        logger.warning("⚠ Endee not reachable — running in fallback mode")

    yield  # App runs here

    logger.info("Shutting down...")


# ── Create app ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    description="AI-powered resume analysis, job matching, and interview prep — powered by Endee vector database",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────
origins = settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ──────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(resume.router)
app.include_router(analysis.router)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "powered_by": "Endee Vector Database",
    }
