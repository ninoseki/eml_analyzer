from pydantic import Field

from .api_model import APIModel


class VerdictDetail(APIModel):
    key: str
    score: float | int | None = Field(default=None)
    description: str
    reference_link: str | None = Field(default=None)


class Verdict(APIModel):
    name: str
    malicious: bool
    score: float | int | None = Field(default=None)
    details: list[VerdictDetail] = Field(default_factory=list)
