from dataclasses import dataclass
from functools import partial
from typing import List, Optional

import aiometer
from loguru import logger

from app.schemas.verdict import Detail, Verdict
from app.services.urlscan import Urlscan


@dataclass
class UrlscanVerdict:
    score: int
    malicious: bool
    uuid: str
    url: str

    @property
    def link(self) -> str:
        return f"https://urlscan.io/result/{self.uuid}"

    @property
    def description(self) -> str:
        return f"{self.url}({self.link}) is malicious."


async def bulk_get_results(uuids: List[str]) -> List[dict]:
    if len(uuids) == 0:
        return []

    api = Urlscan()
    results = await aiometer.run_all([partial(api.result, uuid) for uuid in uuids])
    return [result for result in results if result is not None]


async def get_urlscan_verdicts(url: str) -> List[UrlscanVerdict]:
    api = Urlscan()

    res = await api.search(url)
    if res is None:
        return []

    results = res.get("results", [])
    uuids = [result.get("_id", "") for result in results]
    results = await bulk_get_results(uuids)

    verdicts: List[UrlscanVerdict] = []
    for result in results:
        score = result.get("verdicts", {}).get("overall", {}).get("score")
        malicous = result.get("verdicts", {}).get("overall", {}).get("malicious")
        uuid = result.get("task", {}).get("uuid", "")
        verdicts.append(
            UrlscanVerdict(score=score, malicious=malicous, uuid=uuid, url=url)
        )
    return verdicts


def find_malicous_verdict(verdicts: List[UrlscanVerdict]) -> Optional[UrlscanVerdict]:
    for verdict in verdicts:
        if verdict.malicious:
            return verdict
    return None


class UrlscanVerdictFactory:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.name = "urlscan.io"

    async def to_model(self) -> Verdict:
        malicious_verdicts: List[UrlscanVerdict] = []

        for url in self.urls:
            try:
                verdicts = await get_urlscan_verdicts(url)
                malicious_verdict = find_malicous_verdict(verdicts)
                if malicious_verdict is not None:
                    malicious_verdicts.append(malicious_verdict)
            except Exception as e:
                logger.exception(e)
                continue

        if len(malicious_verdicts) == 0:
            return Verdict(
                name=self.name,
                malicious=False,
                details=[
                    Detail(
                        key="benign",
                        description="There is no malicious URL in bodies.",
                    )
                ],
            )

        details: List[Detail] = []
        details = [
            Detail(
                key=verdict.url, score=verdict.score, description=verdict.description
            )
            for verdict in malicious_verdicts
        ]
        return Verdict(name=self.name, malicious=True, score=100, details=details)

    @classmethod
    async def from_urls(cls, urls: List[str]) -> Verdict:
        obj = cls(urls)
        return await obj.to_model()
