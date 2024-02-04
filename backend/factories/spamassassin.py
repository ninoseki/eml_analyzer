from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas

from .abstract import AbstractAsyncFactory

NAME = "SpamAssassin"


@future_safe
async def report(
    eml_file: bytes, *, client: clients.SpamAssassin
) -> schemas.SpamAssassinReport:
    return await client.report(eml_file)


@future_safe
async def transform(
    report: schemas.SpamAssassinReport, *, name: str = NAME
) -> schemas.Verdict:
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
    @classmethod
    async def call(
        cls, eml_file: bytes, *, client: clients.SpamAssassin
    ) -> schemas.Verdict:
        f_result: FutureResultE[schemas.Verdict] = flow(
            report(eml_file, client=client), bind(transform)
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
