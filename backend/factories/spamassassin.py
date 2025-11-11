from backend import clients, schemas

from .abstract import AbstractAsyncFactory


async def report(
    eml_file: bytes, *, client: clients.SpamAssassin
) -> schemas.SpamAssassinReport:
    return await client.report(eml_file)


def transform(report: schemas.SpamAssassinReport, *, name: str) -> schemas.Verdict:
    details = [
        schemas.VerdictDetail(
            key=detail.name, score=detail.score, description=detail.description
        )
        for detail in report.details
    ]
    score = report.score
    malicious = report.is_spam()
    return schemas.Verdict(
        name=name,
        malicious=malicious,
        score=score,
        details=details,
    )


class SpamAssassinVerdictFactory(AbstractAsyncFactory):
    def __init__(self, client: clients.SpamAssassin, *, name: str = "SpamAssassin"):
        self.client = client
        self.name = name

    async def call(
        self,
        eml_file: bytes,
    ) -> schemas.Verdict:
        got = await report(eml_file, client=self.client)
        return transform(got, name=self.name)
