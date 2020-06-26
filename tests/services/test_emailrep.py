import pytest
import respx

from app.services.emailrep import EmailRep


@pytest.mark.asyncio
@respx.mock
async def test_get(emailrep_response):
    respx.get(
        "https://emailrep.io/bill@microsoft.com", content=emailrep_response,
    )
    emailrep = EmailRep()
    res = await emailrep.get("bill@microsoft.com")
    assert res.email == "bill@microsoft.com"
