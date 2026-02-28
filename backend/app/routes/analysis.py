"""Analysis route — full resume-job matching pipeline."""

import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    SkillMatch,
    InterviewQuestion,
    LearningResource,
)
from app.services.match_engine import calculate_match_score
from app.services.skill_gap import detect_skill_gaps
from app.services.rag_engine import generate_questions
from app.services.recommendation import get_recommendations

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/match", response_model=AnalysisResponse)
async def analyze_match(request: AnalysisRequest):
    """
    Full analysis pipeline:
    1. Calculate match score (Endee cosine similarity)
    2. Detect skill gaps (Endee semantic matching)
    3. Generate interview questions (RAG via Endee)
    4. Recommend learning resources (Endee semantic search)
    """
    try:
        # ── 1. Match score ─────────────────────────────────────────────
        match_result = calculate_match_score(
            request.resume_text, request.job_description
        )

        # ── 2. Skill gaps ─────────────────────────────────────────────
        gap_result = detect_skill_gaps(
            request.resume_text, request.job_description
        )

        # ── 3. Interview questions (RAG) ──────────────────────────────
        all_skills = [s["skill"] for s in gap_result["matched"]] + \
                     [s["skill"] for s in gap_result["missing"]]
        questions = generate_questions(all_skills, request.job_description)

        # ── 4. Learning recommendations ───────────────────────────────
        missing_skill_names = [s["skill"] for s in gap_result["missing"]]
        resources = get_recommendations(missing_skill_names)

        # ── Build response ────────────────────────────────────────────
        matched_skills = [
            SkillMatch(
                skill=s["skill"],
                similarity=min(s.get("similarity", 0.9), 1.0),
                status="matched",
            )
            for s in gap_result["matched"]
        ]
        missing_skills = [
            SkillMatch(
                skill=s["skill"],
                similarity=min(s.get("similarity", 0.0), 1.0),
                status="missing",
            )
            for s in gap_result["missing"]
        ]
        additional_skills = [
            SkillMatch(
                skill=s["skill"],
                similarity=min(s.get("similarity", 0.0), 1.0),
                status="additional",
            )
            for s in gap_result["additional"]
        ]

        interview_questions = [
            InterviewQuestion(
                question=q["question"],
                category=q["category"],
                difficulty=q["difficulty"],
                key_points=q["key_points"],
                relevance_score=min(q.get("relevance_score", 0.5), 1.0),
            )
            for q in questions
        ]

        learning_resources = [
            LearningResource(
                title=r["title"],
                provider=r["provider"],
                url=r["url"],
                skill_area=r["skill_area"],
                relevance_score=min(r.get("relevance_score", 0.5), 1.0),
                resource_type=r["resource_type"],
            )
            for r in resources
        ]

        # Summary
        summary = (
            f"{match_result['label']} — {match_result['score']}% overall compatibility. "
            f"{gap_result['gap_summary']} "
            f"{len(interview_questions)} targeted interview questions generated. "
            f"{len(learning_resources)} learning resources recommended."
        )

        return AnalysisResponse(
            match_score=match_result["score"],
            match_label=match_result["label"],
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            additional_skills=additional_skills,
            interview_questions=interview_questions,
            learning_resources=learning_resources,
            summary=summary,
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}",
        )
