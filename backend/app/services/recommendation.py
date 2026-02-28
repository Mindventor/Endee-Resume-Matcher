"""Learning recommendation engine — uses Endee to find relevant resources."""

import logging
from app.services import embedding_service, endee_service

logger = logging.getLogger(__name__)

# ── Learning resource database ─────────────────────────────────────────

LEARNING_RESOURCES = [
    # Python
    {"id": "lr_001", "title": "Python for Data Science and Machine Learning Bootcamp", "provider": "Udemy", "url": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/", "skill_area": "Python", "resource_type": "course"},
    {"id": "lr_002", "title": "Automate the Boring Stuff with Python", "provider": "Al Sweigart", "url": "https://automatetheboringstuff.com/", "skill_area": "Python", "resource_type": "book"},
    {"id": "lr_003", "title": "Real Python Tutorials", "provider": "Real Python", "url": "https://realpython.com/", "skill_area": "Python", "resource_type": "tutorial"},
    # JavaScript / TypeScript
    {"id": "lr_004", "title": "The Complete JavaScript Course", "provider": "Udemy", "url": "https://www.udemy.com/course/the-complete-javascript-course/", "skill_area": "JavaScript", "resource_type": "course"},
    {"id": "lr_005", "title": "TypeScript Deep Dive", "provider": "Basarat", "url": "https://basarat.gitbook.io/typescript/", "skill_area": "TypeScript", "resource_type": "book"},
    {"id": "lr_006", "title": "JavaScript.info Modern Tutorial", "provider": "javascript.info", "url": "https://javascript.info/", "skill_area": "JavaScript", "resource_type": "tutorial"},
    # React
    {"id": "lr_007", "title": "React — The Complete Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "skill_area": "React", "resource_type": "course"},
    {"id": "lr_008", "title": "Official React Documentation", "provider": "React", "url": "https://react.dev/", "skill_area": "React", "resource_type": "documentation"},
    # Machine Learning / AI
    {"id": "lr_009", "title": "Machine Learning Specialization", "provider": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "skill_area": "Machine Learning", "resource_type": "course"},
    {"id": "lr_010", "title": "Deep Learning Specialization", "provider": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/specializations/deep-learning", "skill_area": "Deep Learning", "resource_type": "course"},
    {"id": "lr_011", "title": "Fast.ai Practical Deep Learning", "provider": "fast.ai", "url": "https://course.fast.ai/", "skill_area": "Deep Learning", "resource_type": "course"},
    {"id": "lr_012", "title": "Hugging Face NLP Course", "provider": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course", "skill_area": "NLP", "resource_type": "course"},
    {"id": "lr_013", "title": "LangChain Documentation & Tutorials", "provider": "LangChain", "url": "https://python.langchain.com/docs/get_started/introduction", "skill_area": "LLM/RAG", "resource_type": "documentation"},
    # Cloud / DevOps
    {"id": "lr_014", "title": "AWS Certified Solutions Architect", "provider": "A Cloud Guru", "url": "https://acloudguru.com/course/aws-certified-solutions-architect-associate", "skill_area": "AWS", "resource_type": "course"},
    {"id": "lr_015", "title": "Docker Mastery", "provider": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "skill_area": "Docker", "resource_type": "course"},
    {"id": "lr_016", "title": "Kubernetes the Hard Way", "provider": "Kelsey Hightower", "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way", "skill_area": "Kubernetes", "resource_type": "tutorial"},
    {"id": "lr_017", "title": "Terraform Up & Running", "provider": "O'Reilly", "url": "https://www.terraformupandrunning.com/", "skill_area": "Terraform", "resource_type": "book"},
    # Databases
    {"id": "lr_018", "title": "Designing Data-Intensive Applications", "provider": "O'Reilly (Martin Kleppmann)", "url": "https://dataintensive.net/", "skill_area": "Databases", "resource_type": "book"},
    {"id": "lr_019", "title": "MongoDB University Courses", "provider": "MongoDB", "url": "https://university.mongodb.com/", "skill_area": "MongoDB", "resource_type": "course"},
    {"id": "lr_020", "title": "Endee Vector Database Documentation", "provider": "Endee", "url": "https://github.com/Mindventor/endee", "skill_area": "Vector Database", "resource_type": "documentation"},
    # System Design
    {"id": "lr_021", "title": "System Design Interview by Alex Xu", "provider": "ByteByteGo", "url": "https://bytebytego.com/", "skill_area": "System Design", "resource_type": "book"},
    {"id": "lr_022", "title": "Grokking the System Design Interview", "provider": "Educative", "url": "https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers", "skill_area": "System Design", "resource_type": "course"},
    # API / Backend
    {"id": "lr_023", "title": "FastAPI Official Tutorial", "provider": "FastAPI", "url": "https://fastapi.tiangolo.com/tutorial/", "skill_area": "FastAPI", "resource_type": "documentation"},
    {"id": "lr_024", "title": "RESTful API Design Best Practices", "provider": "Microsoft", "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design", "skill_area": "API Design", "resource_type": "documentation"},
    # Security
    {"id": "lr_025", "title": "OWASP Web Security Testing Guide", "provider": "OWASP", "url": "https://owasp.org/www-project-web-security-testing-guide/", "skill_area": "Security", "resource_type": "documentation"},
    # Data Engineering
    {"id": "lr_026", "title": "Fundamentals of Data Engineering", "provider": "O'Reilly", "url": "https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/", "skill_area": "Data Engineering", "resource_type": "book"},
    {"id": "lr_027", "title": "Apache Kafka for Beginners", "provider": "Udemy", "url": "https://www.udemy.com/course/apache-kafka/", "skill_area": "Kafka", "resource_type": "course"},
    # Git / Collaboration
    {"id": "lr_028", "title": "Pro Git Book", "provider": "Git", "url": "https://git-scm.com/book/en/v2", "skill_area": "Git", "resource_type": "book"},
    # Mobile
    {"id": "lr_029", "title": "React Native — The Practical Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/react-native-the-practical-guide/", "skill_area": "React Native", "resource_type": "course"},
    {"id": "lr_030", "title": "Flutter & Dart — The Complete Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/", "skill_area": "Flutter", "resource_type": "course"},
]

_seeded = False


def _seed_resources() -> None:
    """Seed learning resources into Endee."""
    global _seeded
    if _seeded:
        return
    _seeded = True

    texts = [
        f"{r['skill_area']} {r['title']} {r['resource_type']} {r['provider']}"
        for r in LEARNING_RESOURCES
    ]
    embeddings = embedding_service.encode_batch(texts)

    vectors = []
    for res, vec in zip(LEARNING_RESOURCES, embeddings):
        vectors.append({
            "id": res["id"],
            "vector": vec,
            "meta": {
                "title": res["title"],
                "provider": res["provider"],
                "url": res["url"],
                "skill_area": res["skill_area"],
                "resource_type": res["resource_type"],
            },
            "filter": {
                "skill_area": res["skill_area"],
                "resource_type": res["resource_type"],
            },
        })

    endee_service.upsert_vectors("learning_resources", vectors)
    logger.info(f"Seeded {len(vectors)} learning resources into Endee")


def get_recommendations(
    missing_skills: list[str],
    top_per_skill: int = 2,
    max_total: int = 10,
) -> list[dict]:
    """
    Recommend learning resources for missing skills using Endee semantic search.
    """
    _seed_resources()

    if not missing_skills:
        return []

    recommendations = []
    seen_ids = set()

    for skill in missing_skills[:10]:  # Limit to avoid too many queries
        query_text = f"Learn {skill} course tutorial documentation"
        query_vec = embedding_service.encode(query_text)

        results = endee_service.query_similar(
            "learning_resources", query_vec, top_k=top_per_skill
        )

        for r in results:
            rid = r.get("id", "")
            if rid in seen_ids:
                continue
            seen_ids.add(rid)

            meta = r.get("meta", {})
            recommendations.append({
                "title": meta.get("title", ""),
                "provider": meta.get("provider", ""),
                "url": meta.get("url", "#"),
                "skill_area": meta.get("skill_area", skill),
                "relevance_score": round(r.get("similarity", 0.0), 3),
                "resource_type": meta.get("resource_type", "course"),
            })

    # Sort by relevance and limit
    recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Fallback if Endee returned nothing
    if not recommendations:
        for skill in missing_skills[:5]:
            for res in LEARNING_RESOURCES:
                if skill.lower() in res["skill_area"].lower() or skill.lower() in res["title"].lower():
                    if res["id"] not in seen_ids:
                        seen_ids.add(res["id"])
                        recommendations.append({
                            "title": res["title"],
                            "provider": res["provider"],
                            "url": res["url"],
                            "skill_area": res["skill_area"],
                            "relevance_score": 0.5,
                            "resource_type": res["resource_type"],
                        })
                        break

    return recommendations[:max_total]
