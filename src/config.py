from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


SWAGGER_PARAMETERS = {
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "displayOperationId": True,
    "filter": True,
    "requestSnippets": True,
    "defaultModelsExpandDepth": -1,
    "docExpansion": "none",
    "persistAuthorization": True,
    "displayRequestDuration": True,
}


class Settings(BaseSettings):
    db_url: PostgresDsn
    redis_url: RedisDsn

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"), case_sensitive=False, extra="ignore"
    )


settings = Settings()
