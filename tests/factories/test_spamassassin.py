import pytest

from backend import clients, factories


@pytest.mark.asyncio
async def test_sample(sample_eml: bytes, spam_assassin: clients.SpamAssassin):
    verdict = await factories.SpamAssassinVerdictFactory.call(
        sample_eml, client=spam_assassin
    )
    assert verdict.malicious is False
    assert len(verdict.details) > 0
