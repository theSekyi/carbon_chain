import logging
import sys
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    """

    environment: str = "dev"
    testing: bool = 0
    database_url: AnyUrl = None


@lru_cache()
def get_settings() -> BaseSettings:
    """
    Load application settings from environment variables and return a Settings instance.
    """
    log.info("Loading config settings from the environment...")
    return Settings()
