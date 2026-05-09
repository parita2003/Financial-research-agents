# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "llama3-70b-8192"
    news_api_key: str
    supabase_url: str
    supabase_anon_key: str
    app_env: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()