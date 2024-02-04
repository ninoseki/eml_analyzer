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

    byte_keys: list[bytes] = optional_redis.keys(f"{settings.REDIS_KEY_PREFIX}:*")  # type: ignore
    return [
        byte_key.decode().removeprefix(f"{settings.REDIS_KEY_PREFIX}:")
        for byte_key in byte_keys
    ]
