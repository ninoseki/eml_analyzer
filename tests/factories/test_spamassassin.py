from unittest.mock import AsyncMock

import pytest

from app.factories.spamassassin import SpamAssassinVerdictFactory


@pytest.mark.asyncio
async def test_sample(sample_eml: bytes, spamassassin_response, mocker):
    mock = AsyncMock()
    mock.return_value = spamassassin_response
    mocker.patch("aiospamc.report", mock)

    verdict = await SpamAssassinVerdictFactory.from_bytes(sample_eml)
    assert verdict.malicious is True
    assert len(verdict.details) > 0
