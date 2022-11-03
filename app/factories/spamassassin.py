from dataclasses import dataclass

from loguru import logger

from app.core import settings
from app.schemas.verdict import Detail, Verdict
from app.services.spamassassin import SpamAssassin

HOST = settings.SPAMASSASSIN_HOST
PORT = settings.SPAMASSASSIN_PORT
TIMEOUT = settings.SPAMASSASSIN_TIMEOUT


@dataclass
class Result:
    details: list[Detail]
    score: float
    malicious: bool


class SpamAssassinVerdictFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file
        self.name = "SpamAssassin"

    async def _get_spam_assassin_report(self):
        assassin = SpamAssassin(host=HOST, port=PORT, timeout=TIMEOUT)
        return await assassin.report(self.eml_file)

    async def to_model(self) -> Verdict:
        try:
            report = await self._get_spam_assassin_report()
        except Exception as error:
            logger.exception(error)
            return Verdict(name=self.name, malicious=False, details=[])

        details: list[Detail] = []
        details = [
            Detail(key=detail.name, score=detail.score, description=detail.description)
            for detail in report.details
        ]
        score = report.score
        malicious = report.is_spam()
        return Verdict(
            name=self.name,
            malicious=malicious,
            score=score,
            details=details,
        )

    @classmethod
    async def from_bytes(cls, eml_file: bytes) -> Verdict:
        obj = cls(eml_file)
        return await obj.to_model()
