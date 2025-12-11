import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f".env.{os.getenv('ENVIRONMENT', 'dev')}")
    
    TELEGRAM_API_TOKEN: str

settings = Settings()
