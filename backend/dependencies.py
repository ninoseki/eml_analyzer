import typing
from contextlib import asynccontextmanager, contextmanager

from fastapi import Depends
from redis import Redis
from starlette.datastructures import Secret

from backend import clients, settings
from backend.datastructures import DatabaseURL


@contextmanager
def _get_optional_redis(
    redis_url: DatabaseURL | None = settings.REDIS_URL,
) -> typing.Generator[Redis | None, None, None]:
    if redis_url is None:
        yield None
    else:
        redis: Redis = Redis.from_url(str(redis_url))  # type: ignore
        try:
            yield redis
        finally:
            redis.close()


def get_optional_redis():
    with _get_optional_redis(settings.REDIS_URL) as optional_redis:
        yield optional_redis


@asynccontextmanager
async def _get_optional_vt(api_key: Secret | None = settings.VIRUSTOTAL_API_KEY):
    if api_key is None:
        yield None
    else:
        async with clients.VirusTotal(apikey=str(api_key)) as client:
            yield client


async def get_optional_vt():
    async with _get_optional_vt(settings.VIRUSTOTAL_API_KEY) as client:
        yield client


@asynccontextmanager
async def _get_optional_inquest(api_key: Secret | None = settings.INQUEST_API_KEY):
    if api_key is None:
        yield None
    else:
        async with clients.InQuest(api_key=api_key) as client:
            yield client


async def get_optional_inquest():
    async with _get_optional_inquest(settings.INQUEST_API_KEY) as client:
        yield client


@asynccontextmanager
async def _get_optional_urlscan(api_key: Secret | None = settings.URLSCAN_API_KEY):
    if api_key is None:
        yield None
    else:
        async with clients.UrlScan(api_key=api_key) as client:
            yield client


async def get_optional_urlscan():
    async with _get_optional_urlscan(settings.URLSCAN_API_KEY) as client:
        yield client


@asynccontextmanager
async def _get_optional_email_rep(api_key: Secret | None = settings.EMAIL_REP_API_KEY):
    if api_key is None:
        yield None
    else:
        async with clients.EmailRep(api_key=api_key) as client:
            yield client


async def get_optional_email_rep():
    async with _get_optional_email_rep(settings.EMAIL_REP_API_KEY) as client:
        yield client


def get_spam_assassin() -> clients.SpamAssassin:
    return clients.SpamAssassin(
        host=settings.SPAMASSASSIN_HOST,
        port=settings.SPAMASSASSIN_PORT,
        timeout=settings.SPAMASSASSIN_TIMEOUT,
    )


OptionalRedis = typing.Annotated[Redis | None, Depends(get_optional_redis)]

OptionalInQuest = typing.Annotated[
    clients.InQuest | None, Depends(get_optional_inquest)
]
OptionalVirusTotal = typing.Annotated[
    clients.VirusTotal | None, Depends(get_optional_vt)
]
OptionalUrlScan = typing.Annotated[
    clients.UrlScan | None, Depends(get_optional_urlscan)
]

OptionalEmailRep = typing.Annotated[clients.EmailRep, Depends(get_optional_email_rep)]
SpamAssassin = typing.Annotated[clients.SpamAssassin, Depends(get_spam_assassin)]
