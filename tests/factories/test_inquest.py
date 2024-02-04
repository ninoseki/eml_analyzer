import pytest
import vcr
from starlette.datastructures import Secret

from backend import clients, factories, settings


@pytest.fixture
async def client():
    async with clients.InQuest(
        api_key=settings.INQUEST_API_KEY or Secret("")
    ) as client:
        yield client


@vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/inquest.yaml", filter_headers=["authorization"]
)  # type: ignore
@pytest.mark.asyncio
async def test_inquest_factory(client: clients.InQuest):
    verdict = await factories.InQuestVerdictFactory.call(
        ["e86c5988a3a6640fb90b90b9e9200e4cce0669594dbb5422622946208c124149"],
        client=client,
    )
    assert verdict.malicious is True
