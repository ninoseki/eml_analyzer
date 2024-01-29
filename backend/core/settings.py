import sys

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="eml_analyzer")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

LOG_FILE = config("LOG_FILE", default=sys.stderr)
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("LOG_BACKTRACE", cast=bool, default=True)

SPAMASSASSIN_HOST: str = config("SPAMASSASSIN_HOST", cast=str, default="127.0.0.1")
SPAMASSASSIN_PORT: int = config("SPAMASSASSIN_PORT", cast=int, default=783)
SPAMASSASSIN_TIMEOUT: int = config("SPAMASSASSIN_TIMEOUT", cast=int, default=10)

URLSCAN_API_KEY: Secret = config("URLSCAN_API_KEY", cast=Secret, default="")

VIRUSTOTAL_API_KEY: Secret = config("VIRUSTOTAL_API_KEY", cast=Secret, default="")

INQUEST_API_KEY: Secret = config("INQUEST_API_KEY", cast=Secret, default="")

REDIS_HOST : str = config("REDIS_HOST", cast=str, default="redis")
REDIS_PASSWORD: str = config("REDIS_PASSWORD", cast=str, default="changeme")
REDIS_EXPIRE: str = config("REDIS_EXPIRE", cast=int, default=3600)
