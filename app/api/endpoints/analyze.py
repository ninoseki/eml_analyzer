from fastapi import APIRouter, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.factories.response import ResponseFactory
from app.schemas.payload import FilePayload, Payload
from app.schemas.response import Response

router = APIRouter()


async def _analyze(file: bytes) -> Response:
    try:
        payload = FilePayload(file=file)
    except ValidationError as exc:
        return JSONResponse(
            status_code=422, content=jsonable_encoder({"detail": exc.errors()})
        )

    return await ResponseFactory.from_bytes(payload.file)


@router.post(
    "/",
    response_model=Response,
    response_description="Return an analysis result",
    summary="Analyze an eml",
    description="Analyze an eml and return an analysis result",
    status_code=200,
)
async def analyze(payload: Payload) -> Response:
    return await _analyze(payload.file.encode())


@router.post(
    "/file",
    response_model=Response,
    response_description="Return an analysis result",
    summary="Analyze an eml",
    description="Analyze an eml and return an analysis result",
    status_code=200,
)
async def analyze_file(file: bytes = File(...)) -> Response:
    return await _analyze(file)
