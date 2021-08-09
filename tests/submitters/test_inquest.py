import httpx
import pytest
from respx import MockRouter

from app.schemas.eml import Attachment
from app.submitters.inquest import InQuestSubmitter


@pytest.mark.asyncio
async def test_inquest(
    docx_attachment: Attachment,
    inquest_dfi_upload_response: str,
    respx_mock: MockRouter,
):
    respx_mock.post("https://labs.inquest.net/api/dfi/upload").mock(
        return_value=httpx.Response(200, content=inquest_dfi_upload_response),
    )

    submitter = InQuestSubmitter(docx_attachment)

    result = await submitter.submit()
    assert (
        result.reference_url
        == "https://labs.inquest.net/dfi/sha256/539e4557975be726d0fc8d7813dba5470dd703272957b4476296f976b5678900"
    )
