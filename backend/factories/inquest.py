from functools import partial

import aiometer
from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas, settings, types


@future_safe
async def lookup(sha256: str, *, client: clients.InQuest) -> schemas.InQuestLookup:
    return await client.lookup(sha256)


@future_safe
async def bulk_lookup(
    sha256s: types.ListSet[str],
    *,
    client: clients.InQuest,
    max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
    max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
) -> list[schemas.InQuestLookup]:
    f_results = [lookup(sha256, client=client) for sha256 in set(sha256s)]
    results = await aiometer.run_all(
        [f_result.awaitable for f_result in f_results],
        max_at_once=max_at_once,
        max_per_second=max_per_second,
    )
    values = [unsafe_perform_io(result.value_or(None)) for result in results]
    return [value for value in values if value is not None]


@future_safe
async def transform(lookups: list[schemas.InQuestLookup], *, name: str):
    malicious_lookups = [lookup for lookup in lookups if lookup.malicious]

    if len(malicious_lookups) == 0:
        return schemas.Verdict(
            name=name,
            malicious=False,
            details=[
                schemas.VerdictDetail(
                    key="benign",
                    description="There is no malicious attachment or InQuest doesn't have information about the attachments.",
                )
            ],
        )

    return schemas.Verdict(
        name=name,
        malicious=True,
        score=100,
        details=[
            schemas.VerdictDetail(
                key=lookup.data.sha256,
                description=lookup.description,
                reference_link=lookup.reference_link,
            )
            for lookup in malicious_lookups
        ],
    )


class InQuestVerdictFactory:
    def __init__(self, client: clients.InQuest, *, name: str = "InQuest"):
        self.client = client
        self.name = name

    async def call(
        self,
        sha256s: types.ListSet[str],
        *,
        max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
        max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
    ) -> schemas.Verdict:
        f_result: FutureResultE[schemas.Verdict] = flow(
            bulk_lookup(
                sha256s,
                client=self.client,
                max_at_once=max_at_once,
                max_per_second=max_per_second,
            ),
            bind(partial(transform, name=self.name)),
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
