from typing import List

from loguru import logger

from app.factories.spamassassin import SpamAssassinFactory
from app.schemas.eml import Attachment
from app.schemas.verdict import Verdict


class VerdictsFactory:
    def __init__(self, eml_file: bytes, attachments: List[Attachment] = []):
        self.eml_file = eml_file
        self.attachments = attachments
        self.verdicts: List[Verdict] = []

    def _add_spam_assassin(self):
        try:
            self.verdicts.append(SpamAssassinFactory.from_bytes(self.eml_file))
        except Exception as error:
            logger.error(error)

    def to_model(self) -> List[Verdict]:
        self._add_spam_assassin()
        return self.verdicts

    @classmethod
    def from_bytes__eml(cls, eml_file: bytes) -> List[Verdict]:
        obj = cls(eml_file)
        return obj.to_model()
