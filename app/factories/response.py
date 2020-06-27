from typing import List

from app.factories.eml import EmlFactory
from app.factories.oldid import OleIDVerdictFactory
from app.factories.spamassassin import SpamAssassinVerdictFactory
from app.schemas.response import Response
from app.schemas.verdict import Verdict


class ResponseFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file

    async def to_model(self) -> Response:
        eml = EmlFactory.from_bytes(self.eml_file)

        verdicts: List[Verdict] = []
        verdicts.append(await SpamAssassinVerdictFactory.from_bytes(self.eml_file))
        verdicts.append(OleIDVerdictFactory.from_attachments(eml.attachments))

        return Response(eml=eml, verdicts=verdicts)

    @classmethod
    async def from_bytes(cls, eml_file: bytes) -> Response:
        obj = cls(eml_file)
        return await obj.to_model()
