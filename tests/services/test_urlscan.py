import httpx
import pytest
from respx import MockRouter

from app.services.urlscan import Urlscan


@pytest.mark.asyncio
async def test_search(urlscan_search_response: str, respx_mock: MockRouter):
    respx_mock.get(
        "https://urlscan.io/api/v1/search/?q=task.url%3A%22http%3A%2F%2Frakuten-ia.com%2F%22&size=10",
    ).mock(
        return_value=httpx.Response(200, content=urlscan_search_response),
    )
    api = Urlscan()
    res = await api.search("http://rakuten-ia.com/")
    results = res.get("results")
    assert isinstance(results, list) is True


@pytest.mark.asyncio
async def test_result(urlscan_result_response: str, respx_mock: MockRouter):
    uuid = "3db439ff-036f-409f-96d6-c28da55767f4"
    respx_mock.get(
        "https://urlscan.io/api/v1/result/3db439ff-036f-409f-96d6-c28da55767f4/",
    ).mock(
        return_value=httpx.Response(200, content=urlscan_result_response),
    )
    api = Urlscan()
    res = await api.result(uuid)
    assert res.get("task", {}).get("uuid", "") == uuid
