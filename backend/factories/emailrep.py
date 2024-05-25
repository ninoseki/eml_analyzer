from functools import partial

from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas

from .abstract import AbstractAsyncFactory


@future_safe
async def lookup(email: str, *, client: clients.EmailRep) -> schemas.EmailRepLookup:
    return await client.lookup(email)


@future_safe
async def transform(lookup: schemas.EmailRepLookup, *, key_or_name: str):
    details: list[schemas.VerdictDetail] = []
    malicious = False

    description = f"{lookup.email} is not suspicious. See https://emailrep.io/{lookup.email} for details."
    if lookup.suspicious:
        malicious = True
        description = f"{lookup.email} is suspicious. See https://emailrep.io/{lookup.email} for details."

    details.append(schemas.VerdictDetail(key=key_or_name, description=description))
    return schemas.Verdict(name=key_or_name, malicious=malicious, details=details)


class EmailRepVerdictFactory(AbstractAsyncFactory):
    def __init__(self, client: clients.EmailRep, *, name: str = "EmailRep"):
        self.client = client
        self.name = name

    async def call(self, email: str, key: str | None = None) -> schemas.Verdict:
        key_or_name: str = key or self.name
        f_result: FutureResultE[schemas.Verdict] = flow(
            lookup(email, client=self.client),
            bind(partial(transform, key_or_name=key_or_name)),
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
