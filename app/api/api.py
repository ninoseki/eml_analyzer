from fastapi import APIRouter

from app.api.endpoints import analyze

api_router = APIRouter()
api_router.include_router(analyze.router, prefix="/analyze", tags=["parse"])
