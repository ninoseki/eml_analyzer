from .api_model import APIModel


class Detail(APIModel):
    key: str
    score: float | int | None = None
    description: str
    reference_link: str | None = None


class Verdict(APIModel):
    name: str
    malicious: bool
    score: float | int | None = None
    details: list[Detail]
