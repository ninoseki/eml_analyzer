import pytest
from httpx import AsyncClient

from tests.conftest import read_file


@pytest.mark.asyncio
async def test_analyze(client: AsyncClient):
    payload = {"file": read_file("sample.eml")}
    response = await client.post("/api/analyze/", json=payload)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


@pytest.mark.asyncio
async def test_analyze_with_invalid_file(client: AsyncClient):
    payload = {"file": ""}
    response = await client.post("/api/analyze/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_file(client: AsyncClient):
    data = {"file": read_file("sample.eml").encode()}
    response = await client.post("/api/analyze/file", files=data)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


@pytest.mark.asyncio
async def test_analyze_file_with_invalid_file(client: AsyncClient):
    data = {"file": b""}
    response = await client.post("/api/analyze/file", files=data)

    assert response.status_code == 422
