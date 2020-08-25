import base64
from abc import ABC, abstractmethod
from io import BytesIO

from app.schemas.eml import Attachment
from app.schemas.submission import SubmissionResult


class AbstractSubmitter(ABC):
    def __init__(self, attachment: Attachment):
        self.attachment = attachment

    def attachment_as_file(self) -> BytesIO:
        bytes_ = base64.b64decode(self.attachment.raw)

        file_like = BytesIO(bytes_)
        file_like.name = self.attachment.filename
        return file_like

    @abstractmethod
    async def submit(self) -> SubmissionResult:
        raise NotImplementedError()
