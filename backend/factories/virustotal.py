import contextlib
from functools import partial

import aiometer
import vt

from backend import clients, schemas, settings, types

from .abstract import AbstractAsyncFactory

NAME = "VirusTotal"


async def get_file_object(
    sha256: str, *, client: clients.VirusTotal
) -> vt.Object | None:
    with contextlib.suppress(Exception):
        return await client.get_object_async(f"/files/{sha256}")

    return None


async def bulk_get_file_objects(
    sha256s: types.ListSet[str],
    *,
    client: clients.VirusTotal,
    max_per_second: float | None = settings.ASYNC_MAX_PER_SECOND,
    max_at_once: int | None = settings.ASYNC_MAX_AT_ONCE,
) -> list[vt.Object]:
    tasks = [partial(get_file_object, sha256, client=client) for sha256 in set(sha256s)]
    results = await aiometer.run_all(
        tasks,
        max_at_once=max_at_once,
        max_per_second=max_per_second,
    )
    return [result for result in results if result]


def transform(objects: list[vt.Object], *, name: str = NAME) -> schemas.Verdict:
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
        got = await bulk_get_file_objects(
            sha256s,
            client=self.client,
            max_at_once=max_at_once,
            max_per_second=max_per_second,
        )
        return transform(got, name=self.name)
