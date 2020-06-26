import pathlib

import pytest
import respx

from app.services.emailrep import EmailRep

path = pathlib.Path(__file__).parent / "../fixtures/emailrep.json"
fixture = open(path).read()


@pytest.mark.asyncio
@respx.mock
async def test_get():
    respx.get(
        "https://emailrep.io/bill@microsoft.com", content=fixture,
    )
    emailrep = EmailRep()
    res = await emailrep.get("bill@microsoft.com")
    assert res.email == "bill@microsoft.com"
