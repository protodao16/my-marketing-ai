"""Загрузка конфигурации из переменных окружения (.env)."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Anthropic
    anthropic_api_key: str = ""
    claude_model: str = "claude-opus-4-8"

    # Snov.io
    snov_client_id: str = ""
    snov_client_secret: str = ""
    snov_api_base: str = "https://api.snov.io"

    @property
    def anthropic_ready(self) -> bool:
        return bool(self.anthropic_api_key)

    @property
    def snov_ready(self) -> bool:
        return bool(self.snov_client_id and self.snov_client_secret)


settings = Settings()
