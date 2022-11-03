from functools import partial

import aiometer

from app.core.utils import (
    has_inquest_api_key,
    has_urlscan_api_key,
    has_virustotal_api_key,
)
from app.factories.eml import EmlFactory
from app.factories.inquest import InQuestVerdictFactory
from app.factories.oldid import OleIDVerdictFactory
from app.factories.spamassassin import SpamAssassinVerdictFactory
from app.factories.urlscan import UrlscanVerdictFactory
from app.factories.virustotal import VirusTotalVerdictFactory
from app.schemas.eml import Attachment, Body
from app.schemas.response import Response
from app.schemas.verdict import Verdict


def aggregate_urls_from_bodies(bodies: list[Body]) -> list[str]:
    urls: list[str] = []
    for body in bodies:
        urls.extend(body.urls)
    return list(set(urls))


def aggregate_sha256s_from_attachments(attachments: list[Attachment]) -> list[str]:
    sha256s: list[str] = []
    for attachment in attachments:
        sha256s.append(attachment.hash_.sha256)
    return list(set(sha256s))


class ResponseFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file

    async def to_model(self) -> Response:
        eml = EmlFactory.from_bytes(self.eml_file)
        urls = aggregate_urls_from_bodies(eml.bodies)
        sha256s = aggregate_sha256s_from_attachments(eml.attachments)

        verdicts: list[Verdict] = []

        async_tasks = [
            partial(SpamAssassinVerdictFactory.from_bytes, self.eml_file),
        ]
        if has_urlscan_api_key():
            async_tasks.append(partial(UrlscanVerdictFactory.from_urls, urls))
        if has_virustotal_api_key():
            async_tasks.append(partial(VirusTotalVerdictFactory.from_sha256s, sha256s))
        if has_inquest_api_key():
            async_tasks.append(partial(InQuestVerdictFactory.from_sha256s, sha256s))

        # Add SpamAsassin, urlscan, virustotal verdicts
        verdicts = await aiometer.run_all(async_tasks)
        # Add OleID verdict
        verdicts.append(OleIDVerdictFactory.from_attachments(eml.attachments))
        # Add VT verdict

        return Response(eml=eml, verdicts=verdicts)

    @classmethod
    async def from_bytes(cls, eml_file: bytes) -> Response:
        obj = cls(eml_file)
        return await obj.to_model()
