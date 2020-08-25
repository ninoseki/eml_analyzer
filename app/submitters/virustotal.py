import vt

from app.core.settings import VIRUSTOTAL_API_KEY
from app.schemas.submission import SubmissionResult
from app.submitters.abstract import AbstractSubmitter


class VirusTotalSubmitter(AbstractSubmitter):
    async def submit(self) -> SubmissionResult:
        async with vt.Client(str(VIRUSTOTAL_API_KEY)) as client:
            await client.scan_file_async(self.attachment_as_file())
            sha256 = self.attachment.hash_.sha256
            return SubmissionResult(
                reference_url=f"https://www.virustotal.com/gui/file/{sha256}/detection"
            )
