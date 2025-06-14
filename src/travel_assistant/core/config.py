"""
this file contains centralised application settings which loads once per process.
get_settings() functions is used to access these settings throughout the
application instead of calling os.getenv() directly.

"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, SecretStr

from typing import Literal
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SEED_DIR = PROJECT_ROOT / "seed_data"


class Settings(BaseSettings):
    """this handles all runtime configuration for the service.
    each field is mapped to an environment variable.
    default values are provided for local develoment

    """

    environment: Literal["local", "test", "prod"] = Field(
        "local", env="APP_ENV", description="Runtime environment identifier"
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "CRITICAL"] = Field(
        "INFO", env="LOG_LEVEL"
    )

    # OPENAI CLIENT
    openai_api_key: SecretStr = Field(..., env="OPENAI_API_KEY")
    openai_project_id: str = Field(..., env="OPENAI_PROJECT_ID")
    openai_model: str = Field("gpt-4o", env="OPENAI_MODEL")
    embed_model: str = Field("text-embedding-ada-002", env="EMBED_MODEL")
    openai_timeout: int = Field(30, env="OPENAI_TIMEOUT", ge=5, le=120)
    openai_max_retries: int = Field(3, env="OPENAI_MAX_RETRIES", ge=0, le=10)
    max_prompt_tokens: int = Field(4096, env="MAX_PROMPT_TOKENS", ge=256)
    cost_per_1k_tokens_gbp: float = Field(
        0.008,
        env="COST_PER_1K_TOKENS_GBP",
        description="rough token pricing used for logging of costs (GBP)",
        gt=0,
    )

    project_root: Path = PROJECT_ROOT
    seed_dir: Path = SEED_DIR
    vector_index_path: Path = PROJECT_ROOT / "vector_store.faiss"

    # VALIDATORS
    @field_validator("openai_api_key", mode="after")
    def validate_key(cls, v: SecretStr) -> SecretStr:
        """if a placeholder or an empty key is supplied, fail validation"""

        key = v.get_secret_value().strip()
        if key.lower() in {"", "dummy"}:
            raise ValueError("OPENAI_API_KEY must be set to a real secret key")

        return SecretStr(key)

    # HELPERS
    def estimate_costs(self, /, prompt_tokens: int, completion_tokens: int) -> float:
        """estimation costs for one completion in GBP"""

        total_tokens = prompt_tokens + completion_tokens
        return (total_tokens / 1000) * self.cost_per_1k_tokens_gbp

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        secrets_dir = None


@lru_cache()
def get_settings() -> Settings:
    """ "this function returns a cache settings instance"""
    return Settings()
