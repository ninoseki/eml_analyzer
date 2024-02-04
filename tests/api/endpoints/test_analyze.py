from fastapi import status
from fastapi.testclient import TestClient


def test_analyze(client: TestClient, sample_eml: bytes):
    payload = {"file": sample_eml.decode()}
    response = client.post("/api/analyze/", json=payload)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


def test_analyze_with_invalid_file(client: TestClient):
    payload = {"file": ""}
    response = client.post("/api/analyze/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_analyze_file(client: TestClient, sample_eml: bytes):
    data = {"file": sample_eml}
    response = client.post("/api/analyze/file", files=data)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


def test_analyze_file_with_invalid_file(client: TestClient):
    data = {"file": b""}
    response = client.post("/api/analyze/file", files=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
