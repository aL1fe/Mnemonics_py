import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f".env.{os.getenv('ENVIRONMENT', 'dev')}")

    TELEGRAM_API_TOKEN: str = "DEFAULT_TELEGRAM_API_TOKEN"
    WHISPER_URL: str = "http://127.0.0.1:8006"
    
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""

    # @property
    def DATABASE_URL(self, is_async: bool = False) -> str:
        pg = "asyncpg" if is_async else "psycopg2"  
        return (
            f"postgresql+{pg}://"
            f"{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )
        odbc = "aioodbc" if is_async else "pyodbc"
        return (
            f"mssql+{odbc}:///?odbc_connect="
            "Driver={ODBC Driver 17 for SQL Server};"
            f"Server={self.DB_HOST}\\SQLEXPRESS;"
            f"Database={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASS};"
        )

settings = Settings()
