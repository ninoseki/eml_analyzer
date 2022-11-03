from datetime import datetime
from typing import Optional, Union

from fastapi_utils.api_model import APIModel


class Hash(APIModel):
    md5: str
    sha1: str
    sha256: str
    sha512: str


class Attachment(APIModel):
    raw: str
    filename: str
    size: int
    extension: Optional[str]
    hash_: Hash
    mime_type: str
    mime_type_short: str
    content_header: dict[str, list[Union[str, int]]]

    class Config:
        fields = {"hash_": "hash"}


class Body(APIModel):
    content_type: Optional[str] = None
    hash_: str
    content_header: dict[str, list[Union[str, int]]]
    content: str
    urls: list[str]
    emails: list[str]
    domains: list[str]
    ip_addresses: list[str]

    class Config:
        fields = {"hash_": "hash"}


class Received(APIModel):
    by: Optional[list[str]] = None
    date: datetime
    for_: Optional[list[str]] = None
    from_: Optional[list[str]] = None
    src: str
    with_: Optional[str]
    delay: int

    class Config:
        fields = {"with_": "with", "for_": "for", "from_": "from"}


class Header(APIModel):
    message_id: Optional[str] = None
    subject: str
    defect: Optional[list[str]] = None
    from_: str
    to: list[str]
    cc: Optional[list[str]] = None
    date: Optional[datetime]
    received_email: Optional[list[str]] = None
    received_foremail: Optional[list[str]] = None
    received_domain: Optional[list[str]] = None
    received_ip: Optional[list[str]] = None
    received_src: Optional[str] = None
    received: list[Received]
    header: dict[str, list[Union[str, int]]]

    class Config:
        fields = {"from_": "from"}


class Eml(APIModel):
    attachments: list[Attachment]
    bodies: list[Body]
    header: Header

    class Config:
        fields = {"hash_": "hash"}
