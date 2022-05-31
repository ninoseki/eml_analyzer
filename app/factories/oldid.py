import base64
from typing import List

from loguru import logger

from app.schemas.eml import Attachment
from app.schemas.verdict import Detail, Verdict
from app.services.oleid import OleID


class OleIDVerdictFactory:
    def __init__(self, attachments: List[Attachment]):
        self.attachments = attachments
        self.name = "oleid"

    def _parse_as_ole_file(self, attachment: Attachment) -> List[Detail]:
        details: List[Detail] = []

        data: bytes = base64.b64decode(attachment.raw)
        oleid = OleID(data)
        file_info = f"{attachment.filename}({attachment.hash_.sha256})"
        if oleid.has_vba_macros():
            key = "vba_macros"
            description = f"{file_info} contains VBA macros."
            details.append(Detail(key=key, description=description))

        if oleid.has_flash_objects():
            key = "flash"
            description = f"{file_info} contains Flash objects."
            details.append(Detail(key=key, description=description))

        if oleid.is_encrypted():
            key = "encrypted"
            description = f"{file_info} is encrypted."
            details.append(Detail(key=key, description=description))

        return details

    def to_model(self) -> Verdict:
        details: List[Detail] = []

        for attachment in self.attachments:
            try:
                details.extend(self._parse_as_ole_file(attachment))
            except Exception as error:
                logger.exception(error)

        malicious = len(details) > 0
        if not malicious:
            details.append(
                Detail(
                    key="benign",
                    description="There is no suspicious OLE file in attachments.",
                )
            )
        return Verdict(name=self.name, malicious=malicious, details=details)

    @classmethod
    def from_attachments(cls, attachments: List[Attachment]) -> Verdict:
        obj = cls(attachments)
        return obj.to_model()
