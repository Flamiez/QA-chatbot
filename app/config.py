from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

@lru_cache
def get_settings():
    return Settings()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    embedding_model: str
    qa_model: str
    groq_api_key: str

