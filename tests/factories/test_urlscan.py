import pytest
import respx

from app.factories.urlscan import UrlscanVerdictFactory


@pytest.mark.asyncio
@respx.mock
async def test_urlscan(urlscan_search_response: str, urlscan_result_response: str):
    respx.get(
        "https://urlscan.io/api/v1/search/?q=task.url%3A%22http%3A%2F%2Frakuten-ia.com%2F%22&size=10",
        content=urlscan_search_response,
    )
    respx.get(
        "https://urlscan.io/api/v1/result/3db439ff-036f-409f-96d6-c28da55767f4/",
        content=urlscan_result_response,
    )

    verdict = await UrlscanVerdictFactory.from_urls(["http://rakuten-ia.com/"])
    assert verdict.malicious is True


@pytest.mark.asyncio
@respx.mock
async def test_urlscan_with_empty_response():
    respx.get(
        "https://urlscan.io/api/v1/search/?q=task.url%3A%22http%3A%2F%2Frakuten-ia.com%2F%22&size=10",
        content="{}",
    )

    verdict = await UrlscanVerdictFactory.from_urls(["http://rakuten-ia.com/"])
    assert verdict.malicious is False
