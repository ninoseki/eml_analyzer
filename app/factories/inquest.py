from dataclasses import dataclass, field
from functools import partial
from typing import Optional

import aiometer
from loguru import logger

from app.core.settings import INQUEST_API_KEY
from app.schemas.verdict import Detail, Verdict
from app.services.inquest import InQuest


@dataclass
class InQuestAlert:
    category: str
    description: str
    title: str
    reference: Optional[str]

    @classmethod
    def build(cls, dicts: list[dict]) -> list["InQuestAlert"]:
        return [
            cls(
                category=d.get("category", ""),
                description=d.get("description", ""),
                title=d.get("title", ""),
                reference=d.get("reference"),
            )
            for d in dicts
        ]


@dataclass
class InQuestVerdict:
    sha256: str
    classification: str
    alerts: list[InQuestAlert] = field(default_factory=list)

    @property
    def malicious(self) -> bool:
        return self.classification == "MALICIOUS"

    @property
    def reference_link(self) -> str:
        return f"https://labs.inquest.net/dfi/sha256/{self.sha256}"

    @property
    def description(self) -> str:
        malicious_alerts = [
            alert for alert in self.alerts if alert.category == "malicious"
        ]
        descriptions = [alert.description for alert in malicious_alerts]
        return " / ".join(descriptions)

    @classmethod
    def build(cls, dict_: dict) -> "InQuestVerdict":
        data = dict_.get("data", {})
        sha256 = data.get("sha256", "")
        classification = data.get("classification", "")
        alerts = data.get("inquest_alerts", [])

        return cls(
            sha256=sha256,
            classification=classification,
            alerts=InQuestAlert.build(alerts),
        )


async def get_result(client: InQuest, sha256: str) -> Optional[dict]:
    try:
        return await client.dfi_details(sha256)
    except Exception as e:
        logger.exception(e)
    return None


async def bulk_get_results(sha256s: list[str]) -> list[dict]:
    if len(sha256s) == 0:
        return []

    client = InQuest()
    results = await aiometer.run_all(
        [partial(get_result, client, sha256) for sha256 in sha256s]
    )
    return [result for result in results if result is not None]


async def get_inquest_verdicts(sha256s: list[str]) -> list[InQuestVerdict]:
    if str(INQUEST_API_KEY) == "":
        return []

    results = await bulk_get_results(sha256s)

    verdicts: list[InQuestVerdict] = []
    for result in results:
        verdicts.append(InQuestVerdict.build(result))

    return verdicts


class InQuestVerdictFactory:
    def __init__(self, sha256s: list[str]):
        self.sha256s = sha256s
        self.name = "InQuest"

    async def to_model(self) -> Verdict:
        malicious_verdicts: list[InQuestVerdict] = []

        verdicts = await get_inquest_verdicts(self.sha256s)
        for verdict in verdicts:
            if verdict.malicious:
                malicious_verdicts.append(verdict)

        if len(malicious_verdicts) == 0:
            return Verdict(
                name=self.name,
                malicious=False,
                details=[
                    Detail(
                        key="benign",
                        description="There is no malicious attachment or InQuest doesn't have information about the attachments.",
                    )
                ],
            )

        details: list[Detail] = []
        details = [
            Detail(
                key=verdict.sha256,
                description=verdict.description,
                reference_link=verdict.reference_link,
            )
            for verdict in malicious_verdicts
        ]
        return Verdict(name=self.name, malicious=True, score=100, details=details)

    @classmethod
    async def from_sha256s(cls, sha256s: list[str]) -> Verdict:
        obj = cls(sha256s)
        return await obj.to_model()
