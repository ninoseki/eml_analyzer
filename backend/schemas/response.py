from backend.schemas.eml import Eml
from backend.schemas.verdict import Verdict

from .api_model import APIModel


class Response(APIModel):
    eml: Eml
    verdicts: list[Verdict]
    id: str
