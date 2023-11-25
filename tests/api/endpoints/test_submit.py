import pytest
from pytest_mock import MockerFixture

from backend.schemas.eml import Attachment


@pytest.mark.asyncio
async def test_submit_to_inquest_without_api_key(
    client, docx_attachment: Attachment, mocker: MockerFixture
):
    mocker.patch("backend.core.settings.INQUEST_API_KEY", return_value="")

    payload = docx_attachment.dict()
    response = await client.post("/api/submit/inquest", json=payload)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_submit_to_inquest_with_invalid_extension(
    client, docx_attachment: Attachment
):
    # change extension of the attachment
    docx_attachment.extension = "foo"
    response = await client.post(
        "/api/submit/inquest", json=docx_attachment.model_dump()
    )
    assert response.status_code == 415


@pytest.mark.asyncio
async def test_submit_to_virustotal_without_api_key(
    client, docx_attachment: Attachment, mocker: MockerFixture
):
    mocker.patch("backend.core.settings.VIRUSTOTAL_API_KEY", return_value="")
    response = await client.post(
        "/api/submit/virustotal", json=docx_attachment.model_dump()
    )
    assert response.status_code == 403
