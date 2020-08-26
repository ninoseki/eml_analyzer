import pytest
from pytest_mock import MockerFixture

from app.schemas.eml import Attachment


@pytest.mark.asyncio
async def test_submit_to_inquest_without_api_key(
    client, docx_attachment: Attachment, mocker: MockerFixture
):
    mocker.patch("app.core.settings.INQUEST_API_KEY", return_value="")

    payload = docx_attachment.dict()
    response = await client.post("/api/submit/inquest", json=payload)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_submit_to_inquest_with_invalid_extension(
    client, docx_attachment: Attachment
):
    # change extension of the attachment
    docx_attachment.extension = "foo"

    payload = docx_attachment.dict()
    response = await client.post("/api/submit/inquest", json=payload)

    assert response.status_code == 415


@pytest.mark.asyncio
async def test_submit_to_virustotal_without_api_key(
    client, docx_attachment: Attachment, mocker: MockerFixture
):
    mocker.patch("app.core.settings.VIRUSTOTAL_API_KEY", return_value="")

    payload = docx_attachment.dict()
    response = await client.post("/api/submit/virustotal", json=payload)

    assert response.status_code == 403
