import httpx
import pytest
from respx import MockRouter

from backend.factories.urlscan import UrlscanVerdict, UrlscanVerdictFactory


@pytest.mark.asyncio
async def test_urlscan(
    urlscan_search_response: str, urlscan_result_response: str, respx_mock: MockRouter
):
    uuid = "3db439ff-036f-409f-96d6-c28da55767f4"
    respx_mock.get(
        "https://urlscan.io/api/v1/search/?q=task.url%3A%22http%3A%2F%2Frakuten-ia.com%2F%22&size=10",
    ).mock(return_value=httpx.Response(200, content=urlscan_search_response))
    respx_mock.get(
        f"https://urlscan.io/api/v1/result/{uuid}/",
    ).mock(return_value=httpx.Response(200, content=urlscan_result_response))

    verdict = await UrlscanVerdictFactory.from_urls(["http://rakuten-ia.com/"])
    assert verdict.malicious is True


@pytest.mark.asyncio
async def test_urlscan_with_empty_response(respx_mock: MockRouter):
    respx_mock.get(
        "https://urlscan.io/api/v1/search/?q=task.url%3A%22http%3A%2F%2Frakuten-ia.com%2F%22&size=10",
    ).mock(
        return_value=httpx.Response(200, content="{}"),
    )

    verdict = await UrlscanVerdictFactory.from_urls(["http://rakuten-ia.com/"])
    assert verdict.malicious is False


def test_urlscan_verdict():
    verdict = UrlscanVerdict(
        score=0, malicious=True, uuid="foo", url="http://example.com"
    )
    assert verdict.reference_link == "https://urlscan.io/result/foo/"
