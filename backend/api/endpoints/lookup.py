import json

from redis import StrictRedis
from fastapi import APIRouter, HTTPException, status

from backend.schemas.response import Response
from backend.core.settings import REDIS_HOST, REDIS_PASSWORD

router = APIRouter()

@router.get(
    "/{identifier}/",
    response_description="Return an analysis result",
    summary="Lookup cached analysis",
    description="Try to fetch existing analysis from database",
    status_code=200,
)
async def lookup(identifier: str) -> Response:
    if not REDIS_HOST:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Redis cache is not enabled",
        )

    redis_conn = StrictRedis(host=REDIS_HOST, password=REDIS_PASSWORD)
    data = redis_conn.hget(identifier, "analysis")
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis cache not found",
        )

    return json.loads(data)
