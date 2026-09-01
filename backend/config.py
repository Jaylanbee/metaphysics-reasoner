from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    APP_NAME: str = "Metaphysics-Reasoner API"
    VERSION: str = "3.1.0"
    API_KEY: str = "default_secure_api_key_for_testing"
    DB_PATH: str = "data/ziwei_universe_518k.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMADB_URL: str = "http://localhost:8001"

    # LLM Settings
    LLM_API_KEY: Optional[str] = None
    LLM_ENDPOINT: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
