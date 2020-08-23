from functools import partial
from typing import List

import aiometer

from app.factories.eml import EmlFactory
from app.factories.oldid import OleIDVerdictFactory
from app.factories.spamassassin import SpamAssassinVerdictFactory
from app.factories.urlscan import UrlscanVerdictFactory
from app.schemas.eml import Body
from app.schemas.response import Response
from app.schemas.verdict import Verdict


def aggregate_urls_from_bodies(bodies: List[Body]) -> List[str]:
    urls: List[str] = []
    for body in bodies:
        urls.extend(body.urls)
    return urls


class ResponseFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file

    async def to_model(self) -> Response:
        eml = EmlFactory.from_bytes(self.eml_file)
        urls = aggregate_urls_from_bodies(eml.bodies)

        verdicts: List[Verdict] = []
        # Add SpamAsassin and urlscan verdicts
        verdicts = await aiometer.run_all(
            [
                partial(SpamAssassinVerdictFactory.from_bytes, self.eml_file),
                partial(UrlscanVerdictFactory.from_urls, urls),
            ]
        )
        # Add OleID verdict
        verdicts.append(OleIDVerdictFactory.from_attachments(eml.attachments))

        return Response(eml=eml, verdicts=verdicts)

    @classmethod
    async def from_bytes(cls, eml_file: bytes) -> Response:
        obj = cls(eml_file)
        return await obj.to_model()
