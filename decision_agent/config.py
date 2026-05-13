import os
from dataclasses import dataclass


def _load_dotenv(path: str = ".env") -> None:
    """Tiny .env loader to avoid requiring python-dotenv."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"").strip("'")
            os.environ.setdefault(key, value)


@dataclass
class Settings:
    app_env: str = "dev"
    search_provider: str = "mock"
    llm_provider: str = "rule"
    brave_search_api_key: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"


def _build_settings() -> Settings:
    _load_dotenv(".env")
    return Settings(
        app_env=os.getenv("APP_ENV", "dev"),
        search_provider=os.getenv("SEARCH_PROVIDER", "mock"),
        llm_provider=os.getenv("LLM_PROVIDER", "rule"),
        brave_search_api_key=os.getenv("BRAVE_SEARCH_API_KEY", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    )


settings = _build_settings()
