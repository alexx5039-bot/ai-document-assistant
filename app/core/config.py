from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "postgres"
    postgres_port: int = 5432


    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    upload_dir: Path = Path("uploads/documents")

    redis_url: str = "redis://redis:6379/0"

    mistral_api_key: str
    mistral_model: str = "mistral-small-latest"

    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_price_id: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    @property
    def alembic_database_url(self) -> str:
        return self.database_url.replace(
            "postgresql+asyncpg",
            "postgresql+psycopg",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()