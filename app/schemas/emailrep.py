from typing import Any

from fastapi_utils.api_model import APIModel


class EmailRepResponse(APIModel):
    email: str
    reputation: str
    suspicious: bool
    references: int
    details: dict[str, Any]
