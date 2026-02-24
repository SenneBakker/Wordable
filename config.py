# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    # This tells Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file=".env")


# Create a singleton instance
settings = Settings()