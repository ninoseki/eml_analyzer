import hashlib
from functools import partial

import aiometer
from loguru import logger
from returns.functions import raise_exception
from returns.future import FutureResultE, future_safe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.unsafe import unsafe_perform_io

from backend import clients, schemas, types

from .abstract import AbstractAsyncFactory
from .emailrep import EmailRepVerdictFactory
from .eml import EmlFactory
from .inquest import InQuestVerdictFactory
from .oldid import OleIDVerdictFactory
from .spamassassin import SpamAssassinVerdictFactory
from .urlscan import UrlScanVerdictFactory
from .virustotal import VirusTotalVerdictFactory


def log_exception(exception: Exception):
    logger.exception(exception)


@future_safe
async def parse(eml_file: bytes) -> schemas.Response:
    return schemas.Response(
        eml=EmlFactory.call(eml_file), id=hashlib.sha256(eml_file).hexdigest()
    )


@future_safe
async def get_spam_assassin_verdict(
    eml_file: bytes, *, client: clients.SpamAssassin
) -> schemas.Verdict:
    return await SpamAssassinVerdictFactory.call(eml_file, client=client)


@future_safe
async def get_oleid_verdict(attachments: list[schemas.Attachment]) -> schemas.Verdict:
    return OleIDVerdictFactory.call(attachments)


@future_safe
async def get_email_rep_verdicts(from_, *, client: clients.EmailRep) -> schemas.Verdict:
    return await EmailRepVerdictFactory.call(from_, client=client)


@future_safe
async def get_urlscan_verdict(
    urls: types.ListSet[str], *, client: clients.UrlScan
) -> schemas.Verdict:
    return await UrlScanVerdictFactory.call(urls, client=client)


@future_safe
async def get_inquest_verdict(
    sha256s: types.ListSet[str], *, client: clients.InQuest
) -> schemas.Verdict:
    return await InQuestVerdictFactory.call(sha256s, client=client)


@future_safe
async def get_vt_verdict(
    sha256s: types.ListSet[str], *, client: clients.VirusTotal
) -> schemas.Verdict:
    return await VirusTotalVerdictFactory.call(sha256s, client=client)


@future_safe
async def set_verdicts(
    response: schemas.Response,
    *,
    eml_file: bytes,
    email_rep: clients.EmailRep,
    spam_assassin: clients.SpamAssassin,
    optional_vt: clients.VirusTotal | None = None,
    optional_urlscan: clients.UrlScan | None = None,
    optional_inquest: clients.InQuest | None = None,
) -> schemas.Response:
    f_results: list[FutureResultE[schemas.Verdict]] = [
        get_spam_assassin_verdict(eml_file, client=spam_assassin),
        get_oleid_verdict(response.eml.attachments),
    ]

    if response.eml.header.from_ is not None:
        f_results.append(
            get_email_rep_verdicts(response.eml.header.from_, client=email_rep)
        )

    if optional_vt is not None:
        f_results.append(get_vt_verdict(response.sha256s, client=optional_vt))

    if optional_inquest is not None:
        f_results.append(get_inquest_verdict(response.sha256s, client=optional_inquest))

    if optional_urlscan is not None:
        f_results.append(get_urlscan_verdict(response.urls, client=optional_urlscan))

    results = await aiometer.run_all([f_result.awaitable for f_result in f_results])
    values = [
        unsafe_perform_io(result.alt(log_exception).value_or(None))
        for result in results
    ]
    response.verdicts = [value for value in values if value is not None]
    return response


class ResponseFactory(
    AbstractAsyncFactory,
):
    @classmethod
    async def call(
        cls,
        eml_file: bytes,
        *,
        email_rep: clients.EmailRep,
        spam_assassin: clients.SpamAssassin,
        optional_vt: clients.VirusTotal | None = None,
        optional_urlscan: clients.UrlScan | None = None,
        optional_inquest: clients.InQuest | None = None,
    ) -> schemas.Response:
        f_result: FutureResultE[schemas.Response] = flow(
            parse(eml_file),
            bind(
                partial(
                    set_verdicts,
                    eml_file=eml_file,
                    email_rep=email_rep,
                    spam_assassin=spam_assassin,
                    optional_vt=optional_vt,
                    optional_urlscan=optional_urlscan,
                    optional_inquest=optional_inquest,
                )
            ),
        )
        result = await f_result.awaitable()
        return unsafe_perform_io(result.alt(raise_exception).unwrap())
