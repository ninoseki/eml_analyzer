from typing import Optional

from fastapi_utils.api_model import APIModel


class SubmissionResult(APIModel):
    reference_url: str
    status: Optional[str]
