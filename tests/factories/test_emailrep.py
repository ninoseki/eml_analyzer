import pytest
import respx

from app.factories.emailrep import EmailRepVerdictFactory


@pytest.mark.asyncio
@respx.mock
async def test_bill(emailrep_response):
    respx.get(
        "https://emailrep.io/bill@microsoft.com", content=emailrep_response,
    )

    verdict = await EmailRepVerdictFactory.from_email("bill@microsoft.com")
    assert verdict.malicious is False
    assert len(verdict.details) == 1
    assert "is not suspicious" in verdict.details[0].description
