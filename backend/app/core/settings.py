import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables.

    Uses python-dotenv to read a local .env file if present.
    """

    app_name: str = Field(default="tic-tac-toe-backend")
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # CORS
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    # Database
    database_url: Optional[str] = Field(default=None)

    # AI
    gemini_api_key: Optional[str] = Field(default=None)
    gemini_model: str = Field(default="gemini-2.0-flash")

    class Config:
        extra = "ignore"

    @classmethod
    def from_env(cls) -> "Settings":
        origins_raw = os.getenv("CORS_ORIGINS", "*")
        origins = (
            [o.strip() for o in origins_raw.split(",") if o.strip()]
            if origins_raw and origins_raw != "*"
            else ["*"]
        )

        return cls(
            app_name=os.getenv("APP_NAME", "tic-tac-toe-backend"),
            environment=os.getenv("ENVIRONMENT", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            cors_origins=origins,
            database_url=os.getenv("DATABASE_URL"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        )
