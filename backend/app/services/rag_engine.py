"""RAG engine — retrieval-augmented interview question generation using Endee."""

import logging
from app.services import embedding_service, endee_service

logger = logging.getLogger(__name__)

# ── Pre-built interview question bank ──────────────────────────────────
# These are seeded into Endee and retrieved via semantic similarity

QUESTION_BANK = [
    # Python / General Programming
    {"id": "iq_001", "question": "Explain the difference between a list and a tuple in Python. When would you use each?", "category": "Python", "difficulty": "Easy", "key_points": ["Mutability differences", "Performance implications", "Use cases: tuples for fixed data, lists for dynamic collections"]},
    {"id": "iq_002", "question": "How does Python's garbage collection work? Explain reference counting and the generational GC.", "category": "Python", "difficulty": "Hard", "key_points": ["Reference counting mechanism", "Cyclic reference detection", "Three generations of objects", "gc module usage"]},
    {"id": "iq_003", "question": "What are decorators in Python? Provide a practical example of when you'd use one.", "category": "Python", "difficulty": "Medium", "key_points": ["Function wrapping concept", "Closure mechanics", "@syntax sugar", "Practical uses: logging, auth, timing"]},
    {"id": "iq_004", "question": "Explain async/await in Python. How does asyncio differ from threading?", "category": "Python", "difficulty": "Hard", "key_points": ["Event loop concept", "Coroutines vs threads", "I/O-bound vs CPU-bound", "GIL implications"]},
    # JavaScript / TypeScript
    {"id": "iq_005", "question": "Explain the event loop in JavaScript. How do microtasks and macrotasks differ?", "category": "JavaScript", "difficulty": "Hard", "key_points": ["Call stack and task queue", "Microtask queue (Promises)", "Macrotask queue (setTimeout)", "Rendering pipeline"]},
    {"id": "iq_006", "question": "What is the difference between 'var', 'let', and 'const' in JavaScript?", "category": "JavaScript", "difficulty": "Easy", "key_points": ["Scope differences (function vs block)", "Hoisting behavior", "Reassignment rules", "Best practices"]},
    {"id": "iq_007", "question": "How does prototypal inheritance work in JavaScript? Compare it with class-based inheritance.", "category": "JavaScript", "difficulty": "Medium", "key_points": ["Prototype chain", "__proto__ vs prototype", "Object.create()", "ES6 classes as syntactic sugar"]},
    # React
    {"id": "iq_008", "question": "Explain the React component lifecycle. How do hooks like useEffect map to lifecycle methods?", "category": "React", "difficulty": "Medium", "key_points": ["Mount, update, unmount phases", "useEffect cleanup function", "Dependency array behavior", "Strict mode double-invoke"]},
    {"id": "iq_009", "question": "What is the virtual DOM in React? How does reconciliation work?", "category": "React", "difficulty": "Medium", "key_points": ["Virtual DOM tree diffing", "Fiber architecture", "Key prop importance", "Batched updates"]},
    {"id": "iq_010", "question": "How would you optimize performance in a large React application?", "category": "React", "difficulty": "Hard", "key_points": ["React.memo and useMemo", "Code splitting with lazy/Suspense", "Virtualization for long lists", "State management optimization"]},
    # Machine Learning / AI
    {"id": "iq_011", "question": "Explain the bias-variance tradeoff. How do you diagnose and address underfitting vs overfitting?", "category": "Machine Learning", "difficulty": "Medium", "key_points": ["Bias: systematic error", "Variance: sensitivity to training data", "Learning curves analysis", "Regularization techniques"]},
    {"id": "iq_012", "question": "What is a Transformer architecture? Explain self-attention and its significance.", "category": "Deep Learning", "difficulty": "Hard", "key_points": ["Query-Key-Value mechanism", "Multi-head attention", "Positional encoding", "Advantages over RNNs/LSTMs"]},
    {"id": "iq_013", "question": "How would you build a RAG (Retrieval-Augmented Generation) system? What are the key components?", "category": "AI/NLP", "difficulty": "Hard", "key_points": ["Document chunking strategy", "Embedding model selection", "Vector database for retrieval", "Prompt engineering for generation", "Evaluation metrics"]},
    {"id": "iq_014", "question": "Explain the difference between supervised, unsupervised, and reinforcement learning with examples.", "category": "Machine Learning", "difficulty": "Easy", "key_points": ["Labeled vs unlabeled data", "Classification/regression examples", "Clustering/dimensionality reduction", "Agent-environment interaction"]},
    # System Design
    {"id": "iq_015", "question": "Design a URL shortening service like bit.ly. What are the key considerations?", "category": "System Design", "difficulty": "Hard", "key_points": ["Hashing vs counter approach", "Database choice and indexing", "Caching strategy", "Analytics and rate limiting", "Horizontal scaling"]},
    {"id": "iq_016", "question": "How would you design a real-time notification system at scale?", "category": "System Design", "difficulty": "Hard", "key_points": ["WebSocket vs SSE vs polling", "Message queue architecture", "Fan-out strategies", "Delivery guarantees", "Push notification integration"]},
    # DevOps / Cloud
    {"id": "iq_017", "question": "Explain the difference between Docker containers and virtual machines. When would you choose each?", "category": "DevOps", "difficulty": "Medium", "key_points": ["OS-level vs hardware-level virtualization", "Resource efficiency comparison", "Isolation guarantees", "Use case scenarios"]},
    {"id": "iq_018", "question": "What is Kubernetes? Explain pods, services, and deployments.", "category": "DevOps", "difficulty": "Medium", "key_points": ["Container orchestration", "Pod as smallest deployable unit", "Service discovery and load balancing", "Rolling updates and rollbacks"]},
    {"id": "iq_019", "question": "How would you implement a CI/CD pipeline for a microservices architecture?", "category": "DevOps", "difficulty": "Hard", "key_points": ["Pipeline stages: build, test, deploy", "Container registry workflow", "Blue-green / canary deployments", "Infrastructure as code", "Monitoring and rollback"]},
    # Databases
    {"id": "iq_020", "question": "Compare SQL and NoSQL databases. When would you choose one over the other?", "category": "Databases", "difficulty": "Medium", "key_points": ["ACID vs BASE properties", "Schema rigidity vs flexibility", "Scaling: vertical vs horizontal", "Consistency models", "Query pattern suitability"]},
    {"id": "iq_021", "question": "What is a vector database? How does it differ from traditional databases, and what are its use cases?", "category": "Databases", "difficulty": "Medium", "key_points": ["High-dimensional vector storage", "ANN search algorithms (HNSW)", "Similarity metrics (cosine, L2)", "AI/ML applications: semantic search, recommendations"]},
    {"id": "iq_022", "question": "How do database indexes work? What are the tradeoffs of adding indexes?", "category": "Databases", "difficulty": "Medium", "key_points": ["B-tree and hash indexes", "Read performance improvement", "Write performance cost", "Index selectivity", "Composite indexes"]},
    # API Design
    {"id": "iq_023", "question": "What are RESTful API design best practices? How do you handle versioning and pagination?", "category": "API Design", "difficulty": "Medium", "key_points": ["Resource-oriented URLs", "HTTP methods semantics", "Status code usage", "Versioning strategies", "Cursor vs offset pagination"]},
    {"id": "iq_024", "question": "Compare REST, GraphQL, and gRPC. When would you use each?", "category": "API Design", "difficulty": "Hard", "key_points": ["Over/under-fetching (REST vs GraphQL)", "Strong typing (gRPC/GraphQL)", "Streaming capabilities", "Performance characteristics", "Tooling ecosystem"]},
    # Data Engineering
    {"id": "iq_025", "question": "Explain the ETL pipeline. How would you design one for processing large volumes of data?", "category": "Data Engineering", "difficulty": "Medium", "key_points": ["Extract, Transform, Load phases", "Batch vs streaming processing", "Data validation and quality", "Idempotency and fault tolerance"]},
    # Security
    {"id": "iq_026", "question": "What is OAuth 2.0? Explain the authorization code flow.", "category": "Security", "difficulty": "Medium", "key_points": ["Resource owner, client, auth server", "Authorization code exchange", "Access and refresh tokens", "PKCE for public clients"]},
    {"id": "iq_027", "question": "How do you prevent common web security vulnerabilities (XSS, CSRF, SQL injection)?", "category": "Security", "difficulty": "Medium", "key_points": ["Input sanitization", "Content Security Policy", "CSRF tokens", "Parameterized queries", "HTTPS and secure headers"]},
    # Behavioral
    {"id": "iq_028", "question": "Describe a challenging technical problem you solved. What was your approach?", "category": "Behavioral", "difficulty": "Medium", "key_points": ["Problem identification", "Research and analysis", "Solution design", "Implementation challenges", "Outcome and lessons"]},
    {"id": "iq_029", "question": "How do you handle disagreements with team members on technical decisions?", "category": "Behavioral", "difficulty": "Easy", "key_points": ["Active listening", "Data-driven arguments", "Prototyping/proof of concept", "Compromise and consensus", "Documentation of decisions"]},
    {"id": "iq_030", "question": "Tell me about a time you had to learn a new technology quickly. How did you approach it?", "category": "Behavioral", "difficulty": "Easy", "key_points": ["Learning strategy", "Resource selection", "Hands-on practice", "Knowledge sharing", "Application to real problems"]},
]

_seeded = False


def _seed_question_bank() -> None:
    """Seed the question bank into Endee for RAG retrieval."""
    global _seeded
    if _seeded:
        return
    _seeded = True

    texts = [
        f"{q['category']} {q['question']} {' '.join(q['key_points'])}"
        for q in QUESTION_BANK
    ]
    embeddings = embedding_service.encode_batch(texts)

    vectors = []
    for q, vec in zip(QUESTION_BANK, embeddings):
        vectors.append({
            "id": q["id"],
            "vector": vec,
            "meta": {
                "question": q["question"],
                "category": q["category"],
                "difficulty": q["difficulty"],
                "key_points": "|".join(q["key_points"]),
            },
            "filter": {
                "category": q["category"],
                "difficulty": q["difficulty"],
            },
        })

    endee_service.upsert_vectors("interview_questions", vectors)
    logger.info(f"Seeded {len(vectors)} interview questions into Endee")


def generate_questions(
    skills: list[str],
    job_description: str,
    top_k: int = 8,
) -> list[dict]:
    """
    Generate interview questions using RAG — retrieves the most relevant
    questions from Endee based on the job description and candidate skills.
    """
    _seed_question_bank()

    # Build a rich query combining JD + skills for better semantic retrieval
    query_text = f"Interview questions for: {job_description[:500]}. Key skills: {', '.join(skills[:20])}"
    query_vec = embedding_service.encode(query_text)

    # ── Retrieve from Endee ────────────────────────────────────────────
    results = endee_service.query_similar("interview_questions", query_vec, top_k=top_k)

    questions = []
    seen_ids = set()

    for r in results:
        qid = r.get("id", "")
        if qid in seen_ids:
            continue
        seen_ids.add(qid)

        meta = r.get("meta", {})
        key_points_str = meta.get("key_points", "")
        key_points = key_points_str.split("|") if key_points_str else []

        questions.append({
            "question": meta.get("question", ""),
            "category": meta.get("category", "General"),
            "difficulty": meta.get("difficulty", "Medium"),
            "key_points": key_points,
            "relevance_score": round(r.get("similarity", 0.0), 3),
        })

    # Sort by relevance
    questions.sort(key=lambda q: q["relevance_score"], reverse=True)

    # If Endee returned few results, add fallback questions
    if len(questions) < 3:
        for q in QUESTION_BANK[:5]:
            if q["id"] not in seen_ids:
                questions.append({
                    "question": q["question"],
                    "category": q["category"],
                    "difficulty": q["difficulty"],
                    "key_points": q["key_points"],
                    "relevance_score": 0.5,
                })

    return questions[:top_k]
