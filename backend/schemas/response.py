import itertools
from functools import cached_property

from pydantic import Field

from .api_model import APIModel
from .eml import Eml
from .verdict import Verdict


class Response(APIModel):
    eml: Eml
    verdicts: list[Verdict] = Field(default_factory=list)
    id: str

    @cached_property
    def urls(self) -> set[str]:
        return set(
            itertools.chain.from_iterable([body.urls for body in self.eml.bodies])
        )

    @cached_property
    def sha256s(self) -> set[str]:
        return {attachment.hash.sha256 for attachment in self.eml.attachments}
