import httpx
import pytest
from respx import MockRouter

from app.services.emailrep import EmailRep


@pytest.mark.asyncio
async def test_get(emailrep_response, respx_mock: MockRouter):
    respx_mock.get("https://emailrep.io/bill@microsoft.com").mock(
        return_value=httpx.Response(200, content=emailrep_response),
    )
    emailrep = EmailRep()
    res = await emailrep.get("bill@microsoft.com")
    assert res.email == "bill@microsoft.com"
