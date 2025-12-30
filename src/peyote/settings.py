"""peyote Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for peyote."""

    model_config = SettingsConfigDict(
        env_prefix="PEYOTE",
        env_file=".env-peyote",
    )
    debug: bool = False
