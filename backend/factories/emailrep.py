from functools import partial

from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas

from .abstract import AbstractAsyncFactory

NAME_OR_KEY = "EmailRep"


@future_safe
async def lookup(email: str, *, client: clients.EmailRep) -> schemas.EmailRepLookup:
    return await client.lookup(email)


@future_safe
async def transform(lookup: schemas.EmailRepLookup, *, name_or_key: str = NAME_OR_KEY):
    details: list[schemas.VerdictDetail] = []
    malicious = False

    description = f"{lookup.email} is not suspicious. See https://emailrep.io/{lookup.email} for details."
    if lookup.suspicious:
        malicious = True
        description = f"{lookup.email} is suspicious. See https://emailrep.io/{lookup.email} for details."

    details.append(schemas.VerdictDetail(key=name_or_key, description=description))
    return schemas.Verdict(name=name_or_key, malicious=malicious, details=details)


class EmailRepVerdictFactory(AbstractAsyncFactory):
    @classmethod
    async def call(
        cls, email: str, *, client: clients.EmailRep, name_or_key: str = NAME_OR_KEY
    ) -> schemas.Verdict:
        f_result: FutureResultE[schemas.Verdict] = flow(
            lookup(email, client=client),
            bind(partial(transform, name_or_key=name_or_key)),
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
