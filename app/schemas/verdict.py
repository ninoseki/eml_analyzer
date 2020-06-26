from typing import List, Optional, Union

from fastapi_utils.api_model import APIModel


class Detail(APIModel):
    key: str
    score: Optional[Union[float, int]]
    description: str


class Verdict(APIModel):
    name: str
    malicious: bool
    score: Optional[Union[float, int]]
    details: List[Detail]
