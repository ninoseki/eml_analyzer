import contextlib
from functools import partial

import aiometer

from backend import clients, schemas, settings, types


async def lookup(
    sha256: str, *, client: clients.InQuest
) -> schemas.InQuestLookup | None:
    with contextlib.suppress(Exception):
        return await client.lookup(sha256)


async def bulk_lookup(
    sha256s: types.ListSet[str],
    *,
    client: clients.InQuest,
    max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
    max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
) -> list[schemas.InQuestLookup]:
    tasks = [partial(lookup, sha256, client=client) for sha256 in set(sha256s)]
    results = await aiometer.run_all(
        tasks,
        max_at_once=max_at_once,
        max_per_second=max_per_second,
    )
    return [result for result in results if result]


def transform(lookups: list[schemas.InQuestLookup], *, name: str):
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
        got = await bulk_lookup(
            sha256s,
            client=self.client,
            max_at_once=max_at_once,
            max_per_second=max_per_second,
        )
        return transform(got, name=self.name)
