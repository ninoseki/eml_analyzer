import pytest

from backend import clients, factories


@pytest.fixture
def factory(spam_assassin: clients.SpamAssassin):
    return factories.SpamAssassinVerdictFactory(spam_assassin)


@pytest.mark.asyncio
async def test_sample(sample_eml: bytes, factory: factories.SpamAssassinVerdictFactory):
    verdict = await factory.call(sample_eml)
    assert verdict.malicious is False
    assert len(verdict.details) > 0
