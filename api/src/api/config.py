from functools import lru_cache
from typing import Any, Dict, List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # MongoDB
    DSSLDRF_CONNSTR: str
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_POOL_SIZE: int = 100

    # Session Settings
    SESSION_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Pydantic V2 configuration
    model_config = SettingsConfigDict(
        # Use absolute path so .env is found regardless of where the script runs
        env_file=".env",
        # Ignores extra fields in your .env like API_VERSION, MONGO_USERNAME, etc.
        extra="ignore",
        case_sensitive=True,
    )

    def get_mongodb_options(self) -> Dict[str, Any]:
        """Get MongoDB client options"""
        return {
            "minPoolSize": self.MONGODB_MIN_POOL_SIZE,
            "maxPoolSize": self.MONGODB_MAX_POOL_SIZE,
            "retryWrites": True,
            "retryReads": True,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
