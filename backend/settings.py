import sys

from starlette.config import Config
from starlette.datastructures import Secret

from .datastructures import DatabaseURL

try:
    config = Config(".env")
except Exception:
    config = Config()

PROJECT_NAME: str = config("PROJECT_NAME", default="eml_analyzer")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

LOG_FILE = config("LOG_FILE", default=sys.stderr)
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("LOG_BACKTRACE", cast=bool, default=True)

# Spam Assassin
SPAMASSASSIN_HOST: str = config("SPAMASSASSIN_HOST", cast=str, default="127.0.0.1")
SPAMASSASSIN_PORT: int = config("SPAMASSASSIN_PORT", cast=int, default=783)
SPAMASSASSIN_TIMEOUT: int = config("SPAMASSASSIN_TIMEOUT", cast=int, default=10)

# Redis
REDIS_URL: DatabaseURL | None = config("REDIS_URL", cast=DatabaseURL, default=None)
REDIS_EXPIRE: int = config("REDIS_EXPIRE", cast=int, default=3600)
REDIS_KEY_PREFIX: str = config("REDIS_KEY_PREFIX", cast=str, default="analysis")
REDIS_CACHE_LIST_AVAILABLE: bool = config("REDIS_CACHE_LIST_AVAILABLE", cast=bool, default=True)

# 3rd party API keys
VIRUSTOTAL_API_KEY: Secret | None = config(
    "VIRUSTOTAL_API_KEY", cast=Secret, default=None
)
INQUEST_API_KEY: Secret | None = config("INQUEST_API_KEY", cast=Secret, default=None)
URLSCAN_API_KEY: Secret | None = config("URLSCAN_API_KEY", cast=Secret, default=None)
EMAIL_REP_API_KEY: Secret | None = config(
    "EMAIL_REP_API_KEY", cast=Secret, default=None
)

# Async/aiometer
ASYNC_MAX_AT_ONCE: int | None = config("ASYNC_MAX_AT_ONCE", cast=int, default=None)
ASYNC_MAX_PER_SECOND: float | None = config(
    "ASYNC_MAX_PER_SECOND", cast=float, default=None
)
