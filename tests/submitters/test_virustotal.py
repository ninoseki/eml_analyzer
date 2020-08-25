import pytest
from aioresponses import aioresponses

from app.schemas.eml import Attachment
from app.submitters.virustotal import VirusTotalSubmitter


@pytest.mark.asyncio
async def test_virustotal(docx_attachment: Attachment):
    submitter = VirusTotalSubmitter(docx_attachment)

    with aioresponses() as aiomock:
        aiomock.get(
            "https://www.virustotal.com/api/v3/files/upload_url",
            payload=dict(data="https://www.virustotal.com/_ah/upload/foo"),
        )

        analysis_data = {"type": "analysis", "id": "foo"}
        aiomock.post(
            "https://www.virustotal.com/_ah/upload/foo",
            payload=dict(data=analysis_data),
        )

        result = await submitter.submit()
        assert (
            result.reference_url
            == "https://www.virustotal.com/gui/file/28df2d6dfa10dc85c8ebb5defffcb15c196dca7b26d4fd6859b9ec75ac60cf9e/detection"
        )
