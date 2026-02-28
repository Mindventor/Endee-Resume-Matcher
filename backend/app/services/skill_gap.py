"""Skill gap detection using Endee semantic similarity."""

import logging
from app.services import embedding_service, endee_service
from app.services.resume_parser import extract_skills

logger = logging.getLogger(__name__)


def _seed_skills_index(skills: list[str]) -> None:
    """Seed the skills index with embeddings for a set of skills."""
    if not skills:
        return
    vectors = []
    embeddings = embedding_service.encode_batch(skills)
    for skill, vec in zip(skills, embeddings):
        vectors.append({
            "id": f"skill_{skill.lower().replace(' ', '_')}",
            "vector": vec,
            "meta": {"skill_name": skill, "category": _categorize_skill(skill)},
        })
    endee_service.upsert_vectors("skills", vectors)


def _categorize_skill(skill: str) -> str:
    """Simple skill categorization."""
    skill_lower = skill.lower()
    categories = {
        "language": ["python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "sql"],
        "framework": ["react", "angular", "vue", "next.js", "django", "flask", "fastapi", "spring", "express", "rails", "laravel"],
        "data_science": ["machine learning", "deep learning", "tensorflow", "pytorch", "pandas", "numpy", "data science", "nlp", "computer vision"],
        "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "serverless"],
        "database": ["postgresql", "mysql", "mongodb", "redis", "elasticsearch", "endee"],
        "soft_skill": ["leadership", "communication", "teamwork", "project management", "mentoring"],
    }
    for cat, keywords in categories.items():
        if skill_lower in keywords:
            return cat
    return "technical"


def detect_skill_gaps(resume_text: str, job_description: str) -> dict:
    """
    Detect skill gaps between resume and job description using Endee
    for semantic similarity matching (not just exact string match).

    Returns {matched, missing, additional, gap_summary}.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # Seed skills into Endee for semantic matching
    all_skills = list(set(resume_skills + jd_skills))
    _seed_skills_index(all_skills)

    # ── Semantic matching via Endee ─────────────────────────────────────
    matched = []
    missing = []
    additional = []

    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)

    # For each JD skill, check if resume has it or a semantic near-match
    for skill in jd_skills:
        if skill.lower() in resume_set:
            matched.append({
                "skill": skill,
                "similarity": 1.0,
                "status": "matched",
                "category": _categorize_skill(skill),
            })
        else:
            # Check semantic similarity via Endee
            skill_vec = embedding_service.encode(skill)
            results = endee_service.query_similar("skills", skill_vec, top_k=3)
            best_match_sim = 0.0
            for r in results:
                meta = r.get("meta", {})
                if meta.get("skill_name", "").lower() in resume_set:
                    best_match_sim = max(best_match_sim, r.get("similarity", 0))

            if best_match_sim > 0.85:
                matched.append({
                    "skill": skill,
                    "similarity": round(best_match_sim, 3),
                    "status": "matched",
                    "category": _categorize_skill(skill),
                })
            else:
                missing.append({
                    "skill": skill,
                    "similarity": round(best_match_sim, 3),
                    "status": "missing",
                    "category": _categorize_skill(skill),
                })

    # Additional skills in resume but not in JD
    for skill in resume_skills:
        if skill.lower() not in jd_set:
            additional.append({
                "skill": skill,
                "similarity": 0.0,
                "status": "additional",
                "category": _categorize_skill(skill),
            })

    coverage = len(matched) / max(len(jd_skills), 1) * 100

    return {
        "matched": matched,
        "missing": missing,
        "additional": additional,
        "total_required": len(jd_skills),
        "total_matched": len(matched),
        "coverage_percent": round(coverage, 1),
        "gap_summary": f"{len(matched)}/{len(jd_skills)} required skills matched ({coverage:.0f}% coverage). {len(missing)} skill gaps identified.",
    }
