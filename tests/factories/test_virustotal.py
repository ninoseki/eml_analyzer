import pytest
import vcr

from app.factories.virustotal import VirusTotalVerdictFactory


@pytest.mark.asyncio
@vcr.use_cassette("tests/fixtures/vcr_cassettes/vt.yaml", filter_headers=["x-apikey"])
async def test_virustotal():
    # eicar file
    verdict = await VirusTotalVerdictFactory.from_sha256s(
        ["275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"]
    )
    assert verdict.malicious is True


@pytest.mark.asyncio
@vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/vt_non_malicious.yaml", filter_headers=["x-apikey"]
)
async def test_virustotal_with_non_malicious_file():
    # empty file
    verdict = await VirusTotalVerdictFactory.from_sha256s(
        ["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"]
    )
    assert verdict.malicious is False
