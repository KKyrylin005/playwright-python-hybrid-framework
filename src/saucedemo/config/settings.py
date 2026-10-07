"""Single source of truth for framework configuration (env vars / .env)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BrowserName = Literal["chromium", "firefox", "webkit"]
TraceMode = Literal["off", "on", "retain-on-failure"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="E2E_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    base_url: str = "https://www.saucedemo.com"

    # Browser
    browser: BrowserName = "chromium"
    headless: bool = True
    slow_mo: int = Field(default=0, ge=0)
    timeout_ms: int = Field(default=10_000, gt=0)
    viewport_width: int = 1920
    viewport_height: int = 1080

    # Failure artifacts
    trace_mode: TraceMode = "retain-on-failure"
    screenshot_on_failure: bool = True
    artifacts_dir: Path = Path("test-results")

    # Credentials (SauceDemo's are public demo values; real projects: no defaults)
    password: SecretStr = SecretStr("secret_sauce")

    @field_validator("base_url")
    @classmethod
    def _strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
