from datetime import datetime

from pydantic import Field

from .api_model import APIModel


class Hash(APIModel):
    md5: str
    sha1: str
    sha256: str
    sha512: str


class Attachment(APIModel):
    raw: str
    filename: str
    size: int
    extension: str | None = None
    hash: Hash
    mime_type: str
    mime_type_short: str
    content_header: dict[str, list[str | int]]


class Body(APIModel):
    content_type: str | None = None
    hash: str
    content_header: dict[str, list[str | int]]
    content: str
    urls: list[str]
    emails: list[str]
    domains: list[str]
    ip_addresses: list[str]


class Received(APIModel):
    by: list[str] | None = None
    date: datetime
    for_: list[str] | None = Field(default=None, alias="for")
    from_: list[str] | None = Field(default=None, alias="from")
    src: str
    with_: str | None = Field(default=None, alias="with")
    delay: int


class Header(APIModel):
    message_id: str | None = None
    subject: str
    defect: list[str] | None = None
    from_: str = Field(..., alias="from")
    to: list[str]
    cc: list[str] | None = None
    date: datetime | None = None
    received_email: list[str] | None = None
    received_foremail: list[str] | None = None
    received_domain: list[str] | None = None
    received_ip: list[str] | None = None
    received_src: str | None = None
    received: list[Received]
    header: dict[str, list[str | int]]


class Eml(APIModel):
    attachments: list[Attachment]
    bodies: list[Body]
    header: Header
