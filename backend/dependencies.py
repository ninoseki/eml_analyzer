import typing

from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from backend import clients, settings


def get_optional_redis(request: Request) -> Redis | None:
    try:
        return request.app.state.redis
    except AttributeError:
        return None


def get_required_redis(
    optional_redis: typing.Annotated[Redis | None, Depends(get_optional_redis)],
) -> Redis:
    if optional_redis is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Redis cache is not enabled",
        )
    return optional_redis


async def get_optional_vt():
    if settings.VIRUSTOTAL_API_KEY:
        async with clients.VirusTotal(
            apikey=str(settings.VIRUSTOTAL_API_KEY)
        ) as client:
            yield client
    else:
        yield None


async def get_optional_urlscan():
    if settings.URLSCAN_API_KEY:
        async with clients.UrlScan(api_key=settings.URLSCAN_API_KEY) as client:
            yield client
    else:
        yield None


async def get_optional_email_rep():
    if settings.EMAIL_REP_API_KEY:
        async with clients.EmailRep(api_key=settings.EMAIL_REP_API_KEY) as client:
            yield client
    else:
        yield None


def get_spam_assassin() -> clients.SpamAssassin:
    return clients.SpamAssassin(
        host=settings.SPAMASSASSIN_HOST,
        port=settings.SPAMASSASSIN_PORT,
        timeout=settings.SPAMASSASSIN_TIMEOUT,
    )


OptionalRedis = typing.Annotated[Redis | None, Depends(get_optional_redis)]
RequiredRedis = typing.Annotated[Redis, Depends(get_required_redis)]
OptionalVirusTotal = typing.Annotated[
    clients.VirusTotal | None, Depends(get_optional_vt)
]
OptionalUrlScan = typing.Annotated[
    clients.UrlScan | None, Depends(get_optional_urlscan)
]
OptionalEmailRep = typing.Annotated[clients.EmailRep, Depends(get_optional_email_rep)]
SpamAssassin = typing.Annotated[clients.SpamAssassin, Depends(get_spam_assassin)]
