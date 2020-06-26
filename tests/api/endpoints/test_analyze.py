import pytest

from tests.utils import read_eml


@pytest.mark.asyncio
async def test_analyze(client):
    payload = {"eml_file": read_eml("sample.eml")}
    response = await client.post("/api/analyze/", json=payload)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"


@pytest.mark.asyncio
async def test_analyze_file(client):
    data = {"file": read_eml("sample.eml").encode()}
    response = await client.post("/api/analyze/file", data=data)

    json = response.json()
    assert json.get("eml", {}).get("header", {}).get("subject") == "Winter promotions"
    assert json.get("eml", {}).get("header", {}).get("from") == "no-reply@example.com"
