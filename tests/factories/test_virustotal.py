import pytest

from backend import clients, factories, settings


@pytest.fixture
async def client():
    async with clients.VirusTotal(
        apikey=str(settings.VIRUSTOTAL_API_KEY or "")
    ) as client:
        yield client


@pytest.fixture
def factory(client: clients.VirusTotal):
    return factories.VirusTotalVerdictFactory(client)


@pytest.mark.skip(reason="VCR cannot handle this...")
@pytest.mark.asyncio
async def test_virus_total_factory(factory: factories.VirusTotalVerdictFactory):
    verdict = await factory.call(
        ["275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"],
    )
    assert verdict.malicious is True
