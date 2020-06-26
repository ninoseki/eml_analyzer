from typing import Any, Dict, List

import arrow
from eml_parser import EmlParser
from ioc_finder import (
    parse_domain_names,
    parse_email_addresses,
    parse_ipv4_addresses,
    parse_urls,
)

from app.schemas.eml import Eml


class EmlFactory:
    def __init__(self, eml_file: bytes):
        self.eml_file = eml_file
        parser = EmlParser(include_raw_body=True, include_attachment_data=True)
        self.parsed = parser.decode_email_bytes(eml_file)

    def _normalize_received(self, received: List[Dict]) -> List[Dict]:
        if len(received) == 0:
            return []

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

    def _normalize_body(self, body: Dict[str, Any]) -> Dict[str, Any]:
        content = body.get("content", "")
        body["urls"] = parse_urls(content, parse_urls_without_scheme=False)
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

    def _normalize_attachment(self, attachment: Dict[str, Any]):
        attachment["content_header"] = self._normalize_key_value_header(
            attachment.get("content_header", {})
        )
        return attachment

    def _normalize_attachments(self):
        # change "attachment" to "attachments"
        attachments = self.parsed.get("attachment", [])
        self.parsed["attachments"] = attachments
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
    def from_bytes(cls, eml_file: bytes) -> Eml:
        obj = cls(eml_file)
        return obj.to_model()
