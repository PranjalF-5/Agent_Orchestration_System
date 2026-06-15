from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agent Orchestration System"
    app_version: str = "0.1.0"
    app_env: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    redis_url: str = "redis://localhost:6379/0"
    postgres_url: str = "postgresql+psycopg://agent:agent@localhost:5432/agent_orchestration"
    otel_service_name: str = "agent-orchestration-system"
    otel_exporter_otlp_endpoint: str = "http://localhost:4318"
    otel_enabled: bool = False
    default_reasoning_model: str = "claude-sonnet"
    default_cheap_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

