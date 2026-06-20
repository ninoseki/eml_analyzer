from fastapi import APIRouter, HTTPException, status

from backend import dependencies, settings

router = APIRouter()


@router.get(
    "/",
    response_description="Return cache keys",
    summary="Get analysis cache keys",
    description="Try to get analysis cache keys",
)
async def cache_keys(redis: dependencies.RequiredRedis) -> list[str]:
    if not settings.REDIS_CACHE_LIST_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Cache listing is disabled",
        )

    prefix = f"{settings.REDIS_KEY_PREFIX}:"
    return [
        byte_key.decode().removeprefix(prefix)
        async for byte_key in redis.scan_iter(match=f"{prefix}*")
    ]
