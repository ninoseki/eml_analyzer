import pytest
import respx

from app.schemas.eml import Attachment
from app.submitters.inquest import InQuestSubmitter


@pytest.mark.asyncio
@respx.mock
async def test_inquest(docx_attachment: Attachment, inquest_dfi_upload_response: str):
    respx.post(
        "https://labs.inquest.net/api/dfi/upload", content=inquest_dfi_upload_response,
    )

    submitter = InQuestSubmitter(docx_attachment)

    result = await submitter.submit()
    assert (
        result.reference_url
        == "https://labs.inquest.net/dfi/sha256/539e4557975be726d0fc8d7813dba5470dd703272957b4476296f976b5678900"
    )
