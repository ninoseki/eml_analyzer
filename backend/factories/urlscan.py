import itertools
from functools import partial

import aiometer
from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas, settings, types

from .abstract import AbstractAsyncFactory

NAME = "urlscan.io"


@future_safe
async def lookup(url: str, *, client: clients.UrlScan) -> schemas.UrlScanLookup:
    return await client.lookup(url)


@future_safe
async def bulk_lookup(
    urls: types.ListSet[str],
    *,
    client: clients.UrlScan,
    max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
    max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
) -> list[schemas.UrlScanLookup]:
    f_results = [lookup(url, client=client) for url in set(urls)]
    results = await aiometer.run_all(
        [f_result.awaitable for f_result in f_results],
        max_at_once=max_at_once,
        max_per_second=max_per_second,
    )
    values = [unsafe_perform_io(result.value_or(None)) for result in results]
    return [value for value in values if value is not None]


@future_safe
async def transform(lookups: list[schemas.UrlScanLookup], *, name: str = NAME):
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
    @classmethod
    async def call(
        cls,
        urls: types.ListSet[str],
        *,
        client: clients.UrlScan,
        name: str = NAME,
        max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
        max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
    ):
        f_result: FutureResultE[schemas.Verdict] = flow(
            bulk_lookup(
                urls,
                client=client,
                max_at_once=max_at_once,
                max_per_second=max_per_second,
            ),
            bind(partial(transform, name=name)),
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
