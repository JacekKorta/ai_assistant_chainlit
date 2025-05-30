from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class ChainlitSettings(BaseSettings):
    # Database settings
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    database_url: str
    
    # Proxy settings
    proxy_api_key: str
    proxy_api_url: str

    model_config = SettingsConfigDict(
        env_prefix="CHAINLIT_",
        env_file="../.env",
        extra="ignore"
    )

class Settings(BaseSettings):
    chainlit: ChainlitSettings = ChainlitSettings() # noqa

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