import contextlib
import itertools
from functools import partial

import aiometer

from backend import clients, schemas, settings, types

from .abstract import AbstractAsyncFactory


async def lookup(url: str, *, client: clients.UrlScan) -> schemas.UrlScanLookup | None:
    with contextlib.suppress(Exception):
        return await client.lookup(url)


async def bulk_lookup(
    urls: types.ListSet[str],
    *,
    client: clients.UrlScan,
    max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
    max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
) -> list[schemas.UrlScanLookup]:
    tasks = [partial(lookup, url=url, client=client) for url in set(urls)]
    results = await aiometer.run_all(
        tasks,
        max_at_once=max_at_once,
        max_per_second=max_per_second,
    )
    return [result for result in results if result]


def transform(lookups: list[schemas.UrlScanLookup], *, name: str):
    results = itertools.chain.from_iterable([lookup.results for lookup in lookups])
    malicious_results = [result for result in results if result.verdicts.malicious]

    if len(malicious_results) == 0:
        return schemas.Verdict(
            name=name,
            malicious=False,
            details=[
                schemas.VerdictDetail(
                    key="benign",
                    description="There is no malicious URL in bodies.",
                )
            ],
        )

    return schemas.Verdict(
        name=name,
        malicious=True,
        score=100,
        details=[
            schemas.VerdictDetail(
                key=result.task.url,
                description=f"{result.task.url} is malicious.",
                reference_link=result.link,
            )
            for result in malicious_results
        ],
    )


class UrlScanVerdictFactory(AbstractAsyncFactory):
    def __init__(self, client: clients.UrlScan, *, name: str = "urlscan.io"):
        self.client = client
        self.name = name

    async def call(
        self,
        urls: types.ListSet[str],
        *,
        max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
        max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
    ):
        got = await bulk_lookup(
            urls,
            client=self.client,
            max_at_once=max_at_once,
            max_per_second=max_per_second,
        )
        return transform(got, name=self.name)
