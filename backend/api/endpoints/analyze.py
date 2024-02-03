from fastapi import APIRouter, BackgroundTasks, File, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from redis import Redis

from backend import deps, schemas
from backend.core import settings
from backend.factories.response import ResponseFactory

router = APIRouter()


async def _analyze(file: bytes) -> schemas.Response:
    try:
        payload = schemas.FilePayload(file=file)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(exc.errors()),
        ) from exc

    return await ResponseFactory.from_bytes(payload.file)


def cache_response(
    redis: Redis,
    response: schemas.Response,
    expire: int = settings.REDIS_EXPIRE,
    field: str = settings.REDIS_FIELD,
):
    redis.hset(name=response.id, key=field, value=response.model_dump_json())

    if expire > 0:
        redis.expire(name=response.id, time=expire)


@router.post(
    "/",
    response_description="Return an analysis result",
    summary="Analyze an eml",
    description="Analyze an eml and return an analysis result",
)
async def analyze(
    payload: schemas.Payload,
    *,
    background_tasks: BackgroundTasks,
    optional_redis: deps.OptionalRedis,
) -> schemas.Response:
    response = await _analyze(payload.file.encode())

    if optional_redis is not None:
        background_tasks.add_task(
            cache_response, redis=optional_redis, response=response
        )

    return response


@router.post(
    "/file",
    response_description="Return an analysis result",
    summary="Analyze an eml",
    description="Analyze an eml and return an analysis result",
)
async def analyze_file(
    file: bytes = File(...),
    *,
    background_tasks: BackgroundTasks,
    optional_redis: deps.OptionalRedis,
) -> schemas.Response:
    response = await _analyze(file)

    if optional_redis is not None:
        background_tasks.add_task(
            cache_response, redis=optional_redis, response=response
        )

    return response
