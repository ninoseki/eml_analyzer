from fastapi import APIRouter

from backend.api.endpoints import analyze, lookup, submit

api_router = APIRouter()
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(submit.router, prefix="/submit", tags=["submit"])
api_router.include_router(lookup.router, prefix="/lookup", tags=["lookup"])
