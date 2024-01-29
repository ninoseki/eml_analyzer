from redis import StrictRedis
from fastapi import APIRouter, File, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from backend.factories.response import ResponseFactory
from backend.schemas.payload import FilePayload, Payload
from backend.schemas.response import Response
import backend.core.settings

router = APIRouter()


async def _analyze(file: bytes) -> Response:
    try:
        payload = FilePayload(file=file)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(exc.errors()),
        ) from exc

    data = await ResponseFactory.from_bytes(payload.file)

    if backend.core.settings.REDIS_HOST:
        redis_conn = StrictRedis(host=backend.core.settings.REDIS_HOST, password=backend.core.settings.REDIS_PASSWORD)
        redis_conn.hset("results", data.identifier, data.json())

    return data


@router.post(
    "/",
    response_description="Return an analysis result",
    summary="Analyze an eml",
    description="Analyze an eml and return an analysis result",
    status_code=200,
)
async def analyze(payload: Payload) -> Response:
    return await _analyze(payload.file.encode())


@router.post(
    "/file",
    response_description="Return an analysis result",
    summary="Analyze an eml",
    description="Analyze an eml and return an analysis result",
    status_code=200,
)
async def analyze_file(file: bytes = File(...)) -> Response:
    return await _analyze(file)
