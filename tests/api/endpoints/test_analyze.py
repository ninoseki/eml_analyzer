import pytest

from tests.conftest import read_file


@pytest.mark.asyncio
async def test_analyze(client):
    payload = {"file": read_file("sample.eml")}
    response = await client.post("/api/analyze/", json=payload)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


@pytest.mark.asyncio
async def test_analyze_with_invalid_file(client):
    payload = {"file": ""}
    response = await client.post("/api/analyze/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_file(client):
    data = {"file": read_file("sample.eml").encode()}
    response = await client.post("/api/analyze/file", data=data)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


@pytest.mark.asyncio
async def test_analyze_file_with_invalid_file(client):
    data = {"file": b""}
    response = await client.post("/api/analyze/file", data=data)

    assert response.status_code == 422
