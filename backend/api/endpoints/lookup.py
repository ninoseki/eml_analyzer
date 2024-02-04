from fastapi import APIRouter, HTTPException, status

from backend import deps, schemas, settings

router = APIRouter()


@router.get(
    "/{id}",
    response_description="Return an analysis result",
    summary="Lookup cached analysis",
    description="Try to fetch existing analysis from database",
)
async def lookup(id: str, *, optional_redis: deps.OptionalRedis) -> schemas.Response:
    if optional_redis is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Redis cache is not enabled",
        )

    got: bytes | None = optional_redis.hget(key=id, name=settings.REDIS_FIELD)  # type: ignore
    if got is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cache not found",
        )

    return schemas.Response.model_validate_json(got.decode())
