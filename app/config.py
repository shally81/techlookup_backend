import os
from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    rate_limit: int = Field(env="RATE_LIMIT", default=10)
    proxies: str | None = Field(env="PROXY_LIST", default=None)

    class Config:
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
