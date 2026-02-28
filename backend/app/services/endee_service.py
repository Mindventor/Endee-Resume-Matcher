"""Endee vector database service — central to all semantic operations."""

import logging
from endee import Endee, Precision
from app.config import settings

logger = logging.getLogger(__name__)

_client: Endee | None = None

# Index configuration
INDEX_CONFIG = {
    "resumes": {
        "dimension": settings.embedding_dimension,
        "space_type": "cosine",
        "precision": Precision.INT8,
    },
    "skills": {
        "dimension": settings.embedding_dimension,
        "space_type": "cosine",
        "precision": Precision.INT8,
    },
    "interview_questions": {
        "dimension": settings.embedding_dimension,
        "space_type": "cosine",
        "precision": Precision.INT8,
    },
    "learning_resources": {
        "dimension": settings.embedding_dimension,
        "space_type": "cosine",
        "precision": Precision.INT8,
    },
}


def get_client() -> Endee:
    """Get or create the Endee client singleton."""
    global _client
    if _client is None:
        if settings.endee_api_token:
            _client = Endee(token=settings.endee_api_token)
        else:
            _client = Endee()
        _client.set_base_url(settings.endee_base_url)
        logger.info(f"Endee client initialized → {settings.endee_base_url}")
    return _client


def ensure_indexes() -> bool:
    """Create all required indexes if they don't exist. Returns connectivity status."""
    try:
        client = get_client()
        existing = []
        try:
            existing = [idx.get("name", "") for idx in (client.list_indexes() or [])]
        except Exception:
            existing = []

        for name, cfg in INDEX_CONFIG.items():
            if name not in existing:
                try:
                    client.create_index(
                        name=name,
                        dimension=cfg["dimension"],
                        space_type=cfg["space_type"],
                        precision=cfg["precision"],
                    )
                    logger.info(f"Created Endee index: {name}")
                except Exception as e:
                    logger.warning(f"Could not create index '{name}': {e}")
        return True
    except Exception as e:
        logger.error(f"Endee connection failed: {e}")
        return False


def check_connection() -> bool:
    """Check if Endee is reachable."""
    try:
        client = get_client()
        client.list_indexes()
        return True
    except Exception:
        return False


def upsert_vectors(index_name: str, vectors: list[dict]) -> bool:
    """
    Upsert vectors into an Endee index.
    Each vector dict: {"id": str, "vector": list[float], "meta": dict, "filter": dict}
    """
    try:
        client = get_client()
        index = client.get_index(name=index_name)
        # Batch in chunks of 1000 (Endee limit)
        for i in range(0, len(vectors), 1000):
            batch = vectors[i : i + 1000]
            index.upsert(batch)
        logger.info(f"Upserted {len(vectors)} vectors into '{index_name}'")
        return True
    except Exception as e:
        logger.error(f"Upsert failed for '{index_name}': {e}")
        return False


def query_similar(
    index_name: str,
    vector: list[float],
    top_k: int = 10,
    filters: list[dict] | None = None,
) -> list[dict]:
    """
    Query Endee for similar vectors.
    Returns list of {id, similarity, meta, filter}.
    """
    try:
        client = get_client()
        index = client.get_index(name=index_name)
        kwargs = {"vector": vector, "top_k": top_k}
        if filters:
            kwargs["filter"] = filters
        results = index.query(**kwargs)
        return results if results else []
    except Exception as e:
        logger.error(f"Query failed for '{index_name}': {e}")
        return []
