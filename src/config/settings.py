from functools import lru_cache
from typing import Literal

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    url: str = Field(
        "sqlite+aiosqlite:///./data/app.db",
        description="SQLAlchemy compatible async database URL",
    )
    pool_size: int = Field(5, ge=1, description="Base connection pool size")
    max_overflow: int = Field(5, ge=0, description="Max overflow connections")


class SecuritySettings(BaseSettings):
    api_key: str = Field(..., description="Primary API key for server-to-server auth")
    allowed_origins: list[str] = Field(default_factory=lambda: ["*"])
    rate_limit_requests: int = Field(60, ge=1)
    rate_limit_window_seconds: int = Field(60, ge=1)


class ObservabilitySettings(BaseSettings):
    log_level: str = Field("INFO")
    sentry_dsn: HttpUrl | None = None


class LLMSettings(BaseSettings):
    base_url: str | None = Field(
        default=None, description="LLM endpoint base URL (e.g., https://api.cursorai.art/v1)"
    )
    api_key: str | None = Field(default=None, description="LLM API key")
    model: str = Field("gpt-4o-mini", description="LLM model name")
    timeout_seconds: float = Field(6.0, ge=1.0, description="LLM request timeout")
    enabled: bool = Field(True, description="Whether to attempt LLM classification when configured")


class AppSettings(BaseSettings):
    app_name: str = Field("Digital Empathy Platform API")
    app_env: Literal["local", "dev", "staging", "prod"] = Field("local")
    debug: bool = Field(True)
    api_prefix: str = Field("/api")

    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings(api_key="demo-key")
    observability: ObservabilitySettings = ObservabilitySettings()
    llm: LLMSettings = LLMSettings()

    model_registry_path: str = Field("./models")
    rules_path: str = Field("./rules")
    redis_url: str = Field("redis://localhost:6379/0")

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
