"""Resume parsing — extract text and skills from PDF/DOCX files."""

import io
import re
import logging
from PyPDF2 import PdfReader
from docx import Document

logger = logging.getLogger(__name__)

# ── Comprehensive skills taxonomy ───────────────────────────────────────

SKILLS_TAXONOMY = {
    # Programming languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
    "dart", "lua", "haskell", "elixir", "clojure", "sql", "bash", "shell",
    # Web frameworks
    "react", "reactjs", "react.js", "angular", "angularjs", "vue", "vuejs",
    "vue.js", "next.js", "nextjs", "nuxt", "nuxtjs", "svelte", "gatsby",
    "express", "expressjs", "fastapi", "flask", "django", "spring", "spring boot",
    "rails", "ruby on rails", "laravel", "asp.net", "node.js", "nodejs",
    # Data / ML / AI
    "machine learning", "deep learning", "artificial intelligence", "ai", "ml",
    "natural language processing", "nlp", "computer vision", "tensorflow",
    "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy", "scipy",
    "matplotlib", "seaborn", "hugging face", "transformers", "langchain",
    "openai", "gpt", "llm", "large language models", "rag",
    "retrieval augmented generation", "vector database", "embeddings",
    "sentence transformers", "bert", "data science", "data analysis",
    "data engineering", "feature engineering", "model deployment",
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "gcp", "google cloud",
    "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
    "ci/cd", "github actions", "gitlab ci", "circleci", "devops",
    "microservices", "serverless", "lambda", "cloudformation",
    # Databases
    "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch",
    "dynamodb", "cassandra", "sqlite", "oracle", "neo4j", "graphql",
    "firebase", "supabase", "endee", "vector database", "pinecone",
    "weaviate", "milvus", "qdrant", "chroma",
    # Tools & Others
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "figma", "sketch", "adobe xd", "postman", "swagger", "rest api",
    "restful", "grpc", "websocket", "oauth", "jwt", "api design",
    "system design", "agile", "scrum", "kanban", "tdd", "bdd",
    "unit testing", "integration testing", "cypress", "selenium",
    "playwright", "jest", "pytest", "mocha", "chai",
    # Soft skills
    "leadership", "communication", "teamwork", "problem solving",
    "critical thinking", "project management", "time management",
    "mentoring", "stakeholder management", "presentation",
    # Data formats & protocols
    "json", "xml", "yaml", "protobuf", "kafka", "rabbitmq",
    "celery", "redis", "nginx", "apache",
    # Mobile
    "ios", "android", "react native", "flutter", "swiftui",
    "jetpack compose", "mobile development",
    # Security
    "cybersecurity", "penetration testing", "owasp", "encryption",
    "ssl", "tls", "security", "compliance", "gdpr", "soc2",
}


def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts).strip()
    except Exception as e:
        logger.error(f"PDF parsing failed: {e}")
        raise ValueError(f"Could not parse PDF: {e}")


def parse_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(text_parts).strip()
    except Exception as e:
        logger.error(f"DOCX parsing failed: {e}")
        raise ValueError(f"Could not parse DOCX: {e}")


def extract_skills(text: str) -> list[str]:
    """Extract skills from text using taxonomy matching."""
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILLS_TAXONOMY:
        # Use word boundary matching for short skills to avoid false positives
        if len(skill) <= 2:
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        else:
            if skill in text_lower:
                found_skills.add(skill)

    # Normalize: capitalize each skill properly
    normalized = sorted([s.title() if len(s) > 3 else s.upper() for s in found_skills])
    return normalized


def parse_resume(filename: str, file_bytes: bytes) -> tuple[str, list[str]]:
    """
    Parse a resume file and extract text + skills.
    Returns (extracted_text, skills_list).
    """
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "pdf":
        text = parse_pdf(file_bytes)
    elif ext in ("docx", "doc"):
        text = parse_docx(file_bytes)
    elif ext == "txt":
        text = file_bytes.decode("utf-8", errors="ignore").strip()
    else:
        raise ValueError(f"Unsupported file format: .{ext}. Use PDF, DOCX, or TXT.")

    if not text or len(text) < 20:
        raise ValueError("Could not extract sufficient text from the resume.")

    skills = extract_skills(text)
    return text, skills
