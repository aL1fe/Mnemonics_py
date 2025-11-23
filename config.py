from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_API_TOKEN: str = "DEFAULT_TELEGRAM_API_TOKEN"

    class Config:
        env_file = ".env.dev"

settings = Settings()
