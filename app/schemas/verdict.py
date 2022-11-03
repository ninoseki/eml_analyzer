from typing import Optional, Union

from fastapi_utils.api_model import APIModel


class Detail(APIModel):
    key: str
    score: Optional[Union[float, int]]
    description: str
    reference_link: Optional[str]


class Verdict(APIModel):
    name: str
    malicious: bool
    score: Optional[Union[float, int]]
    details: list[Detail]
