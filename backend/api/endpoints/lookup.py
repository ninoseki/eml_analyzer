import json

from redis import StrictRedis
from fastapi import APIRouter, HTTPException

from backend.schemas.response import Response
import backend.core.settings

router = APIRouter()

@router.get(
    "/{identifier}/",
    response_description="Return an analysis result",
    summary="Lookup cached analysis",
    description="Try to fetch existing analysis from database",
    status_code=200,
)
async def lookup(identifier: str) -> Response:
    if not backend.core.settings.REDIS_HOST:
        raise HTTPException(502)

    redis_conn = StrictRedis(host=backend.core.settings.REDIS_HOST, password=backend.core.settings.REDIS_PASSWORD)
    data = redis_conn.hget("results", identifier)
    if not data:
        raise HTTPException(404)

    return json.loads(data)
