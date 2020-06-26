import sys

from starlette.config import Config

config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="eml_analyzer")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

LOG_FILE = config("LOG_FILE", default=sys.stderr)
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("LOG_BACKTRACE", cast=bool, default=True)

SPAMASSASSIN_HOST: str = config("SPAMASSASSIN_HOST", cast=str, default="127.0.0.1")
SPAMASSASSIN_PORT: int = config("SPAMASSASSIN_PORT", cast=int, default=783)
