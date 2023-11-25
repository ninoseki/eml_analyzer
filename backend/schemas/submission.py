from .api_model import APIModel


class SubmissionResult(APIModel):
    reference_url: str
    status: str | None = None
