from fastapi import APIRouter, File

from app.factories.response import ResponseFactory
from app.schemas.payload import Payload
from app.schemas.response import Response

router = APIRouter()


@router.post(
    "/",
    response_model=Response,
    response_description="Return a parsed result",
    summary="Parse an eml",
    description="Parse an eml and return a parsed result",
    status_code=200,
)
def analyze(payload: Payload) -> Response:
    eml_file = payload.eml_file.encode()
    return ResponseFactory.from_bytes(eml_file)


@router.post(
    "/file",
    response_model=Response,
    response_description="Return a parsed result",
    summary="Parse an eml",
    description="Parse an eml and return a parsed result",
    status_code=200,
)
def analyze_file(file: bytes = File(...)) -> Response:
    return ResponseFactory.from_bytes(file)
