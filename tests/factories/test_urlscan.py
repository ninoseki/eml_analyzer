import pytest
import vcr
from starlette.datastructures import Secret

from backend import clients, factories, settings


@pytest.fixture
async def client():
    async with clients.UrlScan(
        api_key=settings.URLSCAN_API_KEY or Secret("")
    ) as client:
        yield client


@vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/urlscan.yaml", filter_headers=["api-key"]
)  # type: ignore
@pytest.mark.asyncio
async def test_urlscan_factory(client: clients.UrlScan):
    verdict = await factories.UrlScanVerdictFactory.call(
        ["http://example.com"], client=client
    )
    assert verdict.malicious is False
