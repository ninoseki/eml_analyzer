from fastapi import APIRouter

from backend.api.endpoints import analyze, cache, lookup, status, submit

api_router = APIRouter()
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(submit.router, prefix="/submit", tags=["submit"])
api_router.include_router(lookup.router, prefix="/lookup", tags=["lookup"])
api_router.include_router(cache.router, prefix="/cache", tags=["cache"])
api_router.include_router(status.router, prefix="/status", tags=["status"])
