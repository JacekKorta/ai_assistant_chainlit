from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class OpenAISettings(BaseSettings):
    url: str
    api_key: str

    model_config = SettingsConfigDict(
        env_prefix="OPEN_AI_",
        env_file="../.env",
        extra="ignore"
    )

class Settings(BaseSettings):
    openai: OpenAISettings = OpenAISettings() # noqa

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of Settings.
    """
    return Settings()