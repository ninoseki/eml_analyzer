import datetime
from io import BytesIO
from typing import Any

import dateparser
from eml_parser import EmlParser
from ioc_finder import parse_domain_names, parse_email_addresses, parse_ipv4_addresses

from backend import schemas
from backend.outlookmsgfile_wrapper import Message
from backend.utils import parse_urls_from_body
from backend.validator import is_msg_file

from .abstract import AbstractFactory


def is_inline_forward_attachment(attachment: dict) -> bool:
    content_header = attachment.get("content_header", {})
    content_types: list[str] = content_header.get("content-type", [])
    content_dispositions: list[str] = content_header.get("content-disposition", [])

    is_rfc822 = False
    for content_type in content_types:
        if content_type.startswith("message/rfc822;"):
            is_rfc822 = True
            break

    is_inline = False
    for content_disposition in content_dispositions:
        if content_disposition.startswith("inline;"):
            is_inline = True
            break

    return is_rfc822 and is_inline


def to_eml(data: bytes) -> bytes:
    if is_msg_file(data):
        # assume data is a msg file
        file = BytesIO(data)
        message = Message(file)
        email = message.to_email()
        return email.as_bytes()

    return data


def parse(data: bytes) -> dict:
    parser = EmlParser(include_raw_body=True, include_attachment_data=True)
    return parser.decode_email_bytes(data)


def parse_datetime(
    dt: str | datetime.datetime | None,
) -> datetime.datetime | str | None:
    if isinstance(dt, datetime.datetime):
        return dt

    if isinstance(dt, str):
        return dateparser.parse(dt) or dt

    return None


def _normalize_received_date(received: dict):
    src = received.get("src", "")
    parts: list[str] = src.split(";")
    last_part = parts[-1].strip()

    date = received.get("date")
    if date:
        received["date"] = parse_datetime(date)
    else:
        received["date"] = parse_datetime(last_part)

    return received


def _normalize_received(received: list[dict]) -> list[dict]:
    if len(received) == 0:
        return []

    received = [_normalize_received_date(r) for r in received]
    received.reverse()

    first = received[0]

    optional_base_datetime: datetime.datetime | str | None = None
    first_date = first.get("date")
    if first_date:
        optional_base_datetime = parse_datetime(first_date)

    for r in received:
        optional_datetime: datetime.datetime | str | None = None
        date = r.get("date")
        if date:
            optional_datetime = parse_datetime(date)

        if optional_base_datetime is None or optional_datetime is None:
            continue

        if not isinstance(optional_base_datetime, datetime.datetime) or not isinstance(
            optional_datetime, datetime.datetime
        ):
            continue

        delay = (optional_datetime - optional_base_datetime).seconds
        r["delay"] = delay
        optional_base_datetime = optional_datetime

    return received


def normalize_header(parsed: dict) -> dict:
    header = parsed.get("header", {})
    # set message-id as a top-level attribute
    message_id = header.get("header", {}).get("message-id", [])
    if len(message_id) > 0:
        header["message_id"] = message_id[0]

    received = header.get("received", [])
    header["received"] = _normalize_received(received)
    parsed["header"] = header
    return parsed


def _normalize_body(body: dict[str, Any]) -> dict[str, Any]:
    content = body.get("content", "")
    content_type = body.get("content_type", "")
    body["urls"] = parse_urls_from_body(content, content_type)
    body["emails"] = parse_email_addresses(content)
    body["domains"] = parse_domain_names(content)
    body["ip_addresses"] = parse_ipv4_addresses(content)

    for key in ["uri", "email", "domain", "ip"]:
        body.pop(key, None)

    return body


def normalize_bodies(parsed: dict) -> dict:
    bodies = parsed.get("body", [])
    parsed["bodies"] = [_normalize_body(body) for body in bodies]
    parsed.pop("body", None)
    return parsed


def normalize_attachments(parsed: dict) -> dict:
    # change "attachment" to "attachments"
    attachments = parsed.get("attachment", [])

    non_inline_forward_attachments = []
    for attachment in attachments:
        content_header = attachment.get("content_header", {})
        if content_id := content_header.get("content-id"):
            attachment["content_id"] = content_id[0]

        if not is_inline_forward_attachment(attachment):
            non_inline_forward_attachments.append(attachment)

    parsed["attachments"] = non_inline_forward_attachments
    parsed.pop("attachment", None)
    return parsed


def transform(parsed: dict) -> schemas.Eml:
    return schemas.Eml.model_validate(parsed)


class EmlFactory(AbstractFactory):
    def call(self, data: bytes) -> schemas.Eml:
        eml = to_eml(data)
        parsed = parse(eml)
        parsed = normalize_header(parsed)
        parsed = normalize_attachments(parsed)
        parsed = normalize_bodies(parsed)
        return transform(parsed)
