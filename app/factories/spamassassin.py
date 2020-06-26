from dataclasses import dataclass
from typing import List, Optional

from loguru import logger

from app.schemas.verdict import Detail, Verdict
from app.services.spamassassin import SpamAssassin


@dataclass
class Result:
    details: List[Detail]
    score: float
    malicious: bool


class SpamAssassinVerdictFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file
        self.name = "SpamAssassin"

    def _get_spam_assassin_result(self) -> Result:
        assassin = SpamAssassin(self.eml_file)
        score = assassin.get_score()
        malicious = assassin.is_spam()
        report = assassin.get_report_json()

        details: List[Detail] = []
        for key, value in report.items():
            partscore: float = value.get("partscore", 0.0)
            full_description: str = value.get("description", "")
            description = full_description.split(key)[-1].strip()
            details.append(Detail(key=key, score=partscore, description=description))

        return Result(details=details, score=score, malicious=malicious)

    def to_model(self) -> Verdict:
        result: Optional[Result] = None

        try:
            result = self._get_spam_assassin_result()
        except Exception as error:
            logger.error(error)

        if result is None:
            return Verdict(name=self.name, malicious=False, details=[])

        return Verdict(
            name=self.name,
            malicious=result.malicious,
            score=result.score,
            details=result.details,
        )

    @classmethod
    def from_bytes(cls, eml_file: bytes) -> Verdict:
        obj = cls(eml_file)
        return obj.to_model()
