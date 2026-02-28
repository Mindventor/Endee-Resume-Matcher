"""Resume upload route."""

import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import ResumeUploadResponse
from app.services.resume_parser import parse_resume
from app.services import embedding_service, endee_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume file (PDF, DOCX, or TXT)."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Validate file type
    allowed = {"pdf", "docx", "doc", "txt"}
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}. Allowed: {', '.join(allowed)}",
        )

    # Validate file size (max 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")

    try:
        text, skills = parse_resume(file.filename, contents)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Generate a resume ID and store embedding in Endee
    resume_id = f"resume_{uuid.uuid4().hex[:12]}"
    try:
        vec = embedding_service.encode(text)
        endee_service.upsert_vectors("resumes", [
            {
                "id": resume_id,
                "vector": vec,
                "meta": {
                    "filename": file.filename,
                    "text_preview": text[:300],
                    "skill_count": len(skills),
                },
            }
        ])
    except Exception as e:
        logger.warning(f"Could not store resume in Endee: {e}")

    return ResumeUploadResponse(
        resume_id=resume_id,
        extracted_text=text,
        skills=skills,
    )
