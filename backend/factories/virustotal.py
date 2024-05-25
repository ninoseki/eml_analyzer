from functools import partial

import aiometer
import vt
from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas, settings, types

from .abstract import AbstractAsyncFactory

NAME = "VirusTotal"


@future_safe
async def get_file_object(sha256: str, *, client: clients.VirusTotal) -> vt.Object:
    return await client.get_object_async(f"/files/{sha256}")


@future_safe
async def bulk_get_file_objects(
    sha256s: types.ListSet[str],
    *,
    client: clients.VirusTotal,
    max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
    max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
) -> list[vt.Object]:
    f_results = [get_file_object(sha256, client=client) for sha256 in set(sha256s)]
    results = await aiometer.run_all(
        [f_result.awaitable for f_result in f_results],
        max_at_once=max_at_once,
        max_per_second=max_per_second,
    )
    values = [unsafe_perform_io(result.value_or(None)) for result in results]
    return [value for value in values if value is not None]


@future_safe
async def transform(objects: list[vt.Object], *, name: str = NAME) -> schemas.Verdict:
    details: list[schemas.VerdictDetail] = []

    for obj in objects:
        malicious = int(obj.last_analysis_stats.get("malicious", 0))
        sha256 = str(obj.sha256)
        if malicious == 0:
            continue

        details.append(
            schemas.VerdictDetail(
                key=sha256,
                score=malicious,
                description=f"{malicious} reports say {sha256} is malicious.",
                reference_link=f"https://www.virustotal.com/gui/file/{sha256}/detection",
            )
        )

    if len(details) == 0:
        return schemas.Verdict(
            name=name,
            malicious=False,
            details=[
                schemas.VerdictDetail(
                    key="benign",
                    description="There is no malicious attachment or VirusTotal doesn't have information about the attachments.",
                )
            ],
        )

    return schemas.Verdict(name=name, malicious=True, score=100, details=details)


class VirusTotalVerdictFactory(AbstractAsyncFactory):
    def __init__(self, client: clients.VirusTotal, *, name: str = "VirusTotal"):
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
            bulk_get_file_objects(
                sha256s,
                client=self.client,
                max_at_once=max_at_once,
                max_per_second=max_per_second,
            ),
            bind(partial(transform, name=self.name)),
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
