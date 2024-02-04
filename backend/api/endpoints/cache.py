from fastapi import APIRouter, HTTPException, status

from backend import deps, settings

router = APIRouter()


@router.get(
    "/",
    response_description="Return cache keys",
    summary="Get analysis cache keys",
    description="Try to get analysis cache keys",
)
async def cache_keys(optional_redis: deps.OptionalRedis) -> list[str]:
    if optional_redis is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Redis cache is not enabled",
        )

    return optional_redis.hkeys(settings.REDIS_HSET_KEY)  # type: ignore
