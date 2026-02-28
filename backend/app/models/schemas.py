"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel, Field
from typing import Optional


# ── Resume ──────────────────────────────────────────────────────────────

class ResumeUploadResponse(BaseModel):
    resume_id: str
    extracted_text: str
    skills: list[str]
    message: str = "Resume processed successfully"


# ── Analysis ────────────────────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    resume_text: str = Field(..., min_length=10, description="Full resume text")
    job_description: str = Field(..., min_length=10, description="Job description text")


class SkillMatch(BaseModel):
    skill: str
    similarity: float = Field(ge=0.0, le=1.0)
    status: str  # "matched" | "missing" | "additional"


class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str  # "Easy" | "Medium" | "Hard"
    key_points: list[str]
    relevance_score: float = Field(ge=0.0, le=1.0)


class LearningResource(BaseModel):
    title: str
    provider: str
    url: str
    skill_area: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    resource_type: str  # "course" | "tutorial" | "documentation" | "book"


class AnalysisResponse(BaseModel):
    match_score: float = Field(ge=0.0, le=100.0)
    match_label: str  # "Excellent" | "Good" | "Fair" | "Low"
    matched_skills: list[SkillMatch]
    missing_skills: list[SkillMatch]
    additional_skills: list[SkillMatch]
    interview_questions: list[InterviewQuestion]
    learning_resources: list[LearningResource]
    summary: str


# ── Health ──────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    endee_connected: bool
    embedding_model: str
    version: str = "1.0.0"
