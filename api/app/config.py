from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Terrible API"
    debug: bool = False

    # Mongo / DocumentDB
    mongo_uri: Optional[str] = None
    mongo_db: str = "terrible"

    # OpenTelemetry
    otel_endpoint: Optional[str] = None

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
