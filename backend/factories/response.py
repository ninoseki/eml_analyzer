import hashlib
from collections.abc import Coroutine
from functools import partial
from typing import Any

import aiometer
from loguru import logger

from backend import clients, schemas, types

from .abstract import AbstractAsyncFactory
from .emailrep import EmailRepVerdictFactory
from .eml import EmlFactory
from .oldid import OleIDVerdictFactory
from .spamassassin import SpamAssassinVerdictFactory
from .urlscan import UrlScanVerdictFactory
from .virustotal import VirusTotalVerdictFactory


def log_exception(exception: Exception):
    logger.exception(exception)


def parse(eml_file: bytes) -> schemas.Response:
    return schemas.Response(
        eml=EmlFactory().call(eml_file), id=hashlib.sha256(eml_file).hexdigest()
    )


async def get_spam_assassin_verdict(
    eml_file: bytes, *, client: clients.SpamAssassin
) -> schemas.Verdict | None:
    try:
        return await SpamAssassinVerdictFactory(client).call(eml_file)
    except Exception as e:
        log_exception(e)

    return None


async def get_oleid_verdict(
    attachments: list[schemas.Attachment],
) -> schemas.Verdict | None:
    try:
        return OleIDVerdictFactory().call(attachments)
    except Exception as e:
        log_exception(e)

    return None


async def get_email_rep_verdicts(
    from_, *, client: clients.EmailRep
) -> schemas.Verdict | None:
    try:
        return await EmailRepVerdictFactory(client).call(from_)
    except Exception as e:
        log_exception(e)

    return None


async def get_urlscan_verdict(
    urls: types.ListSet[str], *, client: clients.UrlScan
) -> schemas.Verdict | None:
    try:
        return await UrlScanVerdictFactory(client).call(urls)
    except Exception as e:
        log_exception(e)

    return None


async def get_vt_verdict(
    sha256s: types.ListSet[str], *, client: clients.VirusTotal
) -> schemas.Verdict | None:
    try:
        return await VirusTotalVerdictFactory(client).call(sha256s)
    except Exception as e:
        log_exception(e)

    return None


async def set_verdicts(
    response: schemas.Response,
    *,
    eml_file: bytes,
    spam_assassin: clients.SpamAssassin,
    optional_email_rep: clients.EmailRep | None = None,
    optional_vt: clients.VirusTotal | None = None,
    optional_urlscan: clients.UrlScan | None = None,
) -> schemas.Response:
    tasks: list[partial[Coroutine[Any, Any, schemas.Verdict | None]]] = [
        partial(get_spam_assassin_verdict, eml_file, client=spam_assassin),
        partial(get_oleid_verdict, response.eml.attachments),
    ]

    if response.eml.header.from_ is not None and optional_email_rep is not None:
        tasks.append(
            partial(
                get_email_rep_verdicts,
                response.eml.header.from_,
                client=optional_email_rep,
            )
        )

    if optional_vt:
        tasks.append(partial(get_vt_verdict, response.sha256s, client=optional_vt))

    if optional_urlscan:
        tasks.append(
            partial(get_urlscan_verdict, response.urls, client=optional_urlscan)
        )

    results = await aiometer.run_all(tasks)
    response.verdicts = [result for result in results if result]
    return response


class ResponseFactory(AbstractAsyncFactory):
    @classmethod
    async def call(
        cls,
        eml_file: bytes,
        *,
        spam_assassin: clients.SpamAssassin,
        optional_email_rep: clients.EmailRep | None,
        optional_vt: clients.VirusTotal | None = None,
        optional_urlscan: clients.UrlScan | None = None,
    ) -> schemas.Response:
        parsed = parse(eml_file)
        return await set_verdicts(
            parsed,
            eml_file=eml_file,
            spam_assassin=spam_assassin,
            optional_email_rep=optional_email_rep,
            optional_vt=optional_vt,
            optional_urlscan=optional_urlscan,
        )
