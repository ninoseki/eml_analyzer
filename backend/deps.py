import typing
from contextlib import contextmanager

from fastapi import Depends
from redis import Redis

from backend.core import settings


def cast_optional_str(v: typing.Any | None) -> str | None:
    if v is None:
        return None

    return str(v)


@contextmanager
def _get_optional_redis(
    redis_url: str | None = cast_optional_str(settings.REDIS_URL),
) -> typing.Generator[Redis | None, None, None]:
    if redis_url is None:
        yield None

    redis: Redis = Redis.from_url(redis_url)  # type: ignore
    try:
        yield redis
    finally:
        redis.close()


def get_optional_redis(redis_url: str | None = cast_optional_str(settings.REDIS_URL)):
    with _get_optional_redis(redis_url) as optional_redis:
        yield optional_redis


OptionalRedis = typing.Annotated[Redis | None, Depends(get_optional_redis)]
