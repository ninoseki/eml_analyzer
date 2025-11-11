from fastapi import status
from fastapi.testclient import TestClient

from backend import schemas


def test_submit_to_virustotal_without_api_key(
    client: TestClient, docx_attachment: schemas.Attachment
):
    response = client.post("/api/submit/virustotal", json=docx_attachment.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN
