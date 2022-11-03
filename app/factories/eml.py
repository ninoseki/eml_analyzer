from io import BytesIO
from typing import Any

import arrow
import dateparser
from eml_parser import EmlParser
from ioc_finder import parse_domain_names, parse_email_addresses, parse_ipv4_addresses

from app.schemas.eml import Eml
from app.services.extractor import parse_urls_from_body
from app.services.outlookmsgfile import Message
from app.services.validator import is_eml_file


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


class EmlFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file
        parser = EmlParser(include_raw_body=True, include_attachment_data=True)
        self.parsed = parser.decode_email_bytes(eml_file)

    def _normalize_received_date(self, received: dict):
        date = received.get("date", "")
        if date != "":
            return received

        src = received.get("src", "")
        parts = src.split(";")
        date_ = parts[-1].strip()
        received["date"] = dateparser.parse(date_)
        return received

    def _normalize_received(self, received: list[dict]) -> list[dict]:
        if len(received) == 0:
            return []

        received = [self._normalize_received_date(r) for r in received]
        received.reverse()

        first = received[0]
        base_date = arrow.get(first.get("date", ""))
        for r in received:
            date = arrow.get(r.get("date", ""))
            delay = (date - base_date).seconds
            r["delay"] = delay
            base_date = date

        return received

    def _normalize_header(self):
        header = self.parsed.get("header", {})
        # set message-id as a top-level attribute
        message_id = header.get("header", {}).get("message-id", [])
        if len(message_id) > 0:
            header["message_id"] = message_id[0]

        received = header.get("received", [])
        header["received"] = self._normalize_received(received)
        self.parsed["header"] = header

    def _normalize_body(self, body: dict[str, Any]) -> dict[str, Any]:
        content = body.get("content", "")
        content_type = body.get("content_type", "")
        body["urls"] = parse_urls_from_body(content, content_type)
        body["emails"] = parse_email_addresses(content)
        body["domains"] = parse_domain_names(content)
        body["ip_addresses"] = parse_ipv4_addresses(content)

        for key in ["uri", "email", "domain", "ip"]:
            if key in body:
                del body[key]

        return body

    def _normalize_bodies(self):
        bodies = self.parsed.get("body", [])
        self.parsed["bodies"] = [self._normalize_body(body) for body in bodies]
        del self.parsed["body"]

    def _normalize_attachments(self):
        # change "attachment" to "attachments"
        attachments = self.parsed.get("attachment", [])

        non_inline_forward_attachments = []
        for attachment in attachments:
            if not is_inline_forward_attachment(attachment):
                non_inline_forward_attachments.append(attachment)

        self.parsed["attachments"] = non_inline_forward_attachments
        if "attachment" in self.parsed:
            del self.parsed["attachment"]

    def normalize(self):
        self._normalize_header()
        self._normalize_attachments()
        self._normalize_bodies()

    def to_model(self) -> Eml:
        self.normalize()
        return Eml.parse_obj(self.parsed)

    @classmethod
    def from_bytes(cls, data: bytes) -> Eml:
        if is_eml_file(data):
            obj = cls(data)
            return obj.to_model()

        # assume data is a msg file
        file = BytesIO(data)
        message = Message(file)
        email = message.to_email()
        obj = cls(email.as_bytes())
        return obj.to_model()
