"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Endee vector database
    endee_api_token: str = ""
    endee_base_url: str = "http://localhost:8080/api/v1"

    # Embedding model
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    # CORS
    cors_origins: str = "*"

    # App
    app_name: str = "AI Resume-Job Intelligence Platform"
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
