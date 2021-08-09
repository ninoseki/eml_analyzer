import httpx
import pytest
from respx import MockRouter

from app.factories.emailrep import EmailRepVerdictFactory


@pytest.mark.asyncio
async def test_bill(emailrep_response, respx_mock: MockRouter):
    respx_mock.get("https://emailrep.io/bill@microsoft.com",).mock(
        return_value=httpx.Response(200, content=emailrep_response)
    )

    verdict = await EmailRepVerdictFactory.from_email("bill@microsoft.com")
    assert verdict.malicious is False
    assert len(verdict.details) == 1
    assert "is not suspicious" in verdict.details[0].description
