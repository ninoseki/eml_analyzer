import vt

from backend.core.settings import VIRUSTOTAL_API_KEY
from backend.schemas.submission import SubmissionResult
from backend.submitters.abstract import AbstractSubmitter


class VirusTotalSubmitter(AbstractSubmitter):
    async def submit(self) -> SubmissionResult:
        async with vt.Client(str(VIRUSTOTAL_API_KEY)) as client:
            await client.scan_file_async(self.attachment_as_file())
            sha256 = self.attachment.hash.sha256
            return SubmissionResult(
                reference_url=f"https://www.virustotal.com/gui/file/{sha256}/detection"
            )
