from fastapi_utils.api_model import APIModel

from app.schemas.eml import Eml
from app.schemas.verdict import Verdict


class Response(APIModel):
    eml: Eml
    verdicts: list[Verdict]
