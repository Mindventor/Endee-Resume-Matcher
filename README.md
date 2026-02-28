# Endee-Resume-Matcher
# AI Resume–Job Semantic Intelligence Platform

**Powered by [Endee Vector Database](https://github.com/Mindventor/endee)**

A full-stack AI SaaS platform that semantically analyzes resumes against job descriptions — delivering match scores, skill gap detection, interview questions, and learning recommendations. Every AI feature is powered by vector embeddings stored and queried through the [Endee](https://github.com/Mindventor/endee) vector database.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [AI & Technology Stack](#ai--technology-stack)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)

---

## How It Works

The platform follows a five-stage pipeline, with Endee at the center of every semantic operation:

### 1. Resume Parsing

When a user uploads a resume (PDF, DOCX, or TXT), the backend extracts the raw text using `PyPDF2` or `python-docx`. It then runs the text through a **skills taxonomy** — a curated list of 150+ technical and soft skills — using regex-based matching to identify skills present in the resume.

### 2. Embedding Generation

Both the resume text and the job description are converted into **384-dimensional dense vectors** using [`SentenceTransformers`](https://www.sbert.net/) with the `all-MiniLM-L6-v2` model. This model maps any text into a fixed-size vector where semantically similar texts are close together in vector space.

### 3. Match Scoring via Endee

The resume embedding is **upserted into Endee's `resumes` index**. The job description embedding is then used as a **query vector** against that index. Endee returns a **cosine similarity score** (0–1), which is scaled to a 0–100 match score. This is not keyword matching — it captures semantic meaning, so "Python developer with REST API experience" will score well against a JD asking for "Backend engineer proficient in Python and API design."

If Endee is not available, the system falls back to a local numpy-based cosine similarity computation.

### 4. Skill Gap Analysis via Semantic Search

Simple set intersection (`resume_skills ∩ jd_skills`) catches exact matches, but misses near-synonyms (e.g., "React.js" vs "ReactJS"). To solve this:

- Every extracted skill is **embedded and upserted into Endee's `skills` index**.
- For each JD skill not found by exact match, the system **queries Endee** for the top-3 most similar skill vectors from the resume.
- If the best match has similarity > 0.85, it is counted as a semantic match.
- Skills are categorized into: **Matched**, **Missing**, and **Additional** (in resume but not in JD).

### 5. RAG Interview Questions

The platform uses **Retrieval-Augmented Generation (RAG)** without an LLM — a technique we call **retrieval-only RAG**:

- A curated bank of **30 interview questions** (spanning Python, JavaScript, React, ML/AI, System Design, DevOps, Databases, API Design, Security, and Behavioral) is **embedded and stored in Endee's `interview_questions` index** on first use.
- When analysis runs, the system builds a **composite query** combining the job description + identified skills.
- This query is **embedded and searched against Endee**, retrieving the top-8 most semantically relevant questions.
- Each question includes: category, difficulty level, key discussion points, and a relevance score from Endee.

This approach ensures that a JD asking for "Kubernetes experience for microservices" surfaces Kubernetes and Docker questions, not unrelated SQL questions — because the retrieval is semantic, not keyword-based.

### 6. Learning Recommendations

The same retrieval pattern powers learning recommendations:

- **30 curated learning resources** (courses, books, tutorials, documentation from providers like Coursera, Udemy, O'Reilly, official docs) are embedded and stored in Endee's `learning_resources` index.
- For each **missing skill**, the system queries Endee with `"Learn {skill} course tutorial documentation"` as the search text.
- Endee returns the most semantically relevant resources, ranked by similarity score.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│  Resume Upload → Job Description → Analyze → Results View   │
│  localhost:3000                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │ Axios (proxied /api)
┌──────────────────────────▼──────────────────────────────────┐
│                    Backend (FastAPI)                         │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Resume       │  │ Match Engine │  │ Skill Gap         │  │
│  │ Parser       │  │ (cosine sim) │  │ Detector          │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Embedding    │  │ RAG Engine   │  │ Recommendation    │  │
│  │ Service      │  │ (retrieval)  │  │ Engine            │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬──────────┘  │
│         │                │                    │             │
│  localhost:8000          │                    │             │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  Endee Vector Database                       │
│                                                             │
│  Indexes:                                                   │
│    resumes ─────────── job-resume cosine similarity          │
│    skills ──────────── semantic skill matching               │
│    interview_questions  RAG retrieval for Q&A               │
│    learning_resources── resource recommendation             │
│                                                             │
│  384-dim vectors · cosine distance · INT8 precision          │
│  localhost:8080                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## AI & Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Embeddings** | [SentenceTransformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) | Converts text → 384-dim vectors. Trained on 1B+ sentence pairs. ~80MB model. |
| **Vector Storage & Search** | [Endee](https://github.com/Mindventor/endee) | Stores all vectors (resumes, skills, questions, resources). Provides sub-5ms ANN search with cosine similarity. HNSW algorithm, INT8 quantization. |
| **Semantic Matching** | Endee cosine similarity | Compares resume ↔ JD vectors. Score 0–100. No keyword matching needed. |
| **Skill Gap Detection** | Endee + taxonomy | Extracts skills via 150+ taxonomy, then uses Endee to find semantic near-matches (>0.85 threshold). |
| **Interview Questions** | Retrieval-only RAG via Endee | 30-question bank embedded in Endee. Semantically retrieved based on JD + skills query. No LLM needed. |
| **Learning Recommendations** | Endee semantic search | 30 curated resources embedded in Endee. Retrieved by missing-skill query. |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | Async Python API framework. Pydantic validation, auto-generated OpenAPI docs. |
| **Frontend** | [React](https://react.dev/) + [Tailwind CSS](https://tailwindcss.com/) | Component-based UI with dark zinc theme. Vite for dev/build. |
| **Resume Parsing** | PyPDF2, python-docx | Extracts text from PDF and DOCX files. |

### Why no LLM?

This platform deliberately uses **retrieval-only AI** rather than a generative LLM. The advantages:

- **Deterministic**: Same inputs always produce the same results. No hallucinations.
- **Fast**: Vector search is sub-5ms. No LLM inference latency.
- **Offline-capable**: Runs entirely locally — no OpenAI API key or cloud dependency.
- **Cost-effective**: No per-token charges. Only the embedding model (~80MB) is needed.
- **Auditable**: Every recommendation traces back to a specific vector match with a similarity score.

---

## Features

| Feature | Description |
|---------|-------------|
| **Resume Upload** | Drag-and-drop PDF, DOCX, or TXT. Extracts text + identifies skills. |
| **Match Scoring** | Animated circular progress (0–100) with color-coded interpretation. |
| **Skill Gap Analysis** | Matched / Missing / Additional skills with similarity percentages. |
| **Interview Questions** | 8 most relevant questions via RAG, with category, difficulty, and key points. |
| **Learning Resources** | Curated courses, books, and docs matched to your skill gaps. |
| **Fallback Mode** | Works even without Endee running — falls back to numpy cosine similarity. |
| **API Docs** | Auto-generated Swagger UI at `/docs`. |

---

## API Endpoints

### `GET /api/health`

Returns system status and Endee connectivity.

```json
{
  "status": "healthy",
  "endee_connected": true,
  "embedding_model": "all-MiniLM-L6-v2",
  "version": "1.0.0"
}
```

### `POST /api/resume/upload`

Upload a resume file (multipart form).

**Request**: `multipart/form-data` with field `file`

**Response**:
```json
{
  "resume_id": "resume_a1b2c3d4e5f6",
  "extracted_text": "Full extracted text...",
  "skills": ["Python", "React", "Docker", "Machine Learning"],
  "message": "Resume processed successfully"
}
```

### `POST /api/analysis/match`

Run the full analysis pipeline.

**Request**:
```json
{
  "resume_text": "Experienced Python developer with 5 years...",
  "job_description": "We are looking for a Senior Backend Engineer..."
}
```

**Response**:
```json
{
  "match_score": 72.4,
  "match_label": "Good Match",
  "matched_skills": [
    { "skill": "Python", "similarity": 1.0, "status": "matched" }
  ],
  "missing_skills": [
    { "skill": "Kubernetes", "similarity": 0.31, "status": "missing" }
  ],
  "additional_skills": [
    { "skill": "React", "similarity": 0.0, "status": "additional" }
  ],
  "interview_questions": [
    {
      "question": "Explain async/await in Python...",
      "category": "Python",
      "difficulty": "Hard",
      "key_points": ["Event loop concept", "Coroutines vs threads"],
      "relevance_score": 0.89
    }
  ],
  "learning_resources": [
    {
      "title": "Kubernetes the Hard Way",
      "provider": "Kelsey Hightower",
      "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way",
      "skill_area": "Kubernetes",
      "relevance_score": 0.92,
      "resource_type": "tutorial"
    }
  ],
  "summary": "Good Match — 72.4% overall compatibility..."
}
```

---

## Project Structure

```
Endee/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point + lifespan
│   │   ├── config.py                # Environment-based settings
│   │   ├── models/
│   │   │   └── schemas.py           # Pydantic request/response models
│   │   ├── routes/
│   │   │   ├── health.py            # GET /api/health
│   │   │   ├── resume.py            # POST /api/resume/upload
│   │   │   └── analysis.py          # POST /api/analysis/match
│   │   └── services/
│   │       ├── embedding_service.py # SentenceTransformers wrapper
│   │       ├── endee_service.py     # Endee client + index management
│   │       ├── resume_parser.py     # PDF/DOCX text extraction + skills
│   │       ├── match_engine.py      # Cosine similarity scoring
│   │       ├── skill_gap.py         # Semantic skill gap detection
│   │       ├── rag_engine.py        # RAG interview question retrieval
│   │       └── recommendation.py    # Learning resource recommendation
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css                # Design system (zinc + emerald)
│   │   ├── api/client.js            # Axios API client
│   │   ├── components/
│   │   │   ├── Layout.jsx           # Sidebar + responsive layout
│   │   │   ├── ResumeUpload.jsx     # Drag-and-drop file upload
│   │   │   ├── JobDescription.jsx   # Text input + analyze button
│   │   │   ├── MatchScore.jsx       # Animated SVG circular progress
│   │   │   ├── SkillGapCards.jsx    # Skill chips + coverage bar
│   │   │   ├── InterviewAccordion.jsx # Expandable Q&A accordion
│   │   │   ├── LearningCards.jsx    # Resource recommendation grid
│   │   │   └── LoadingSpinner.jsx   # Analysis loading overlay
│   │   └── pages/
│   │       └── Dashboard.jsx        # Main page orchestrating all components
│   ├── vite.config.js
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Endee** running on port 8080 (optional — app works in fallback mode)

### Backend

```bash
cd backend
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The first run downloads the `all-MiniLM-L6-v2` model (~80MB).

API docs available at: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

The Vite dev server proxies all `/api` requests to the backend on port 8000.

---

## Docker Deployment

The project uses the [`endeeio/endee-server`](https://hub.docker.com/r/endeeio/endee-server) Docker image as documented in the [Mindventor/endee](https://github.com/Mindventor/endee) fork.

```bash
docker-compose up --build
```

This starts three services:

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `endee` | `endeeio/endee-server:latest` | 8080 | Endee vector database |
| `backend` | Built from `./backend` | 8000 | FastAPI application |
| `frontend` | Built from `./frontend` | 3000 | React app served via Nginx |

---

## Environment Variables

Configure in `backend/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENDEE_API_TOKEN` | _(empty)_ | Endee auth token (maps to `NDD_AUTH_TOKEN`). Leave empty for no-auth mode. |
| `ENDEE_BASE_URL` | `http://localhost:8080/api/v1` | Endee server URL. |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | SentenceTransformers model name. |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated). |

---

## Endee Indexes

The backend automatically creates these indexes on startup:

| Index | Dimension | Distance | Purpose |
|-------|-----------|----------|---------|
| `resumes` | 384 | cosine | Store resume embeddings for match scoring |
| `skills` | 384 | cosine | Store skill embeddings for semantic gap detection |
| `interview_questions` | 384 | cosine | Store Q&A embeddings for RAG retrieval |
| `learning_resources` | 384 | cosine | Store resource embeddings for recommendations |

All indexes use `INT8` precision for memory efficiency.

---

Built with [Endee](https://github.com/Mindventor/endee) · [FastAPI](https://fastapi.tiangolo.com) · [SentenceTransformers](https://www.sbert.net) · [React](https://react.dev) · [Tailwind CSS](https://tailwindcss.com)

