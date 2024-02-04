import pytest

from backend import clients, factories, settings


@pytest.fixture
async def client():
    async with clients.VirusTotal(
        apikey=str(settings.VIRUSTOTAL_API_KEY or "")
    ) as client:
        yield client


@pytest.mark.skip(reason="VCR cannot handle this...")
@pytest.mark.asyncio
async def test_virus_total_factory(client: clients.VirusTotal):
    verdict = await factories.VirusTotalVerdictFactory.call(
        ["275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"],
        client=client,
    )
    assert verdict.malicious is True
