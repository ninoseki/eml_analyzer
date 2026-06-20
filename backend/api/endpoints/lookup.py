from fastapi import APIRouter, HTTPException, status

from backend import dependencies, schemas, settings

router = APIRouter()


@router.get(
    "/{id}",
    response_description="Return an analysis result",
    summary="Lookup cached analysis",
    description="Try to fetch existing analysis from database",
)
async def lookup(id: str, *, redis: dependencies.RequiredRedis) -> schemas.Response:
    got: bytes | None = await redis.get(f"{settings.REDIS_KEY_PREFIX}:{id}")
    if got is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cache not found",
        )

    return schemas.Response.model_validate_json(got.decode())
