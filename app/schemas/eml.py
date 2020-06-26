from datetime import datetime
from typing import Dict, List, Optional, Union

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
    extension: str
    hash_: Hash
    mime_type: str
    mime_type_short: str
    content_header: Dict[str, List[Union[str, int]]]

    class Config:
        fields = {"hash_": "hash"}


class Body(APIModel):
    content_type: Optional[str]
    hash_: str
    content_header: Dict[str, List[Union[str, int]]]
    content: str
    urls: List[str]
    emails: List[str]
    domains: List[str]
    ip_addresses: List[str]

    class Config:
        fields = {"hash_": "hash"}


class Received(APIModel):
    by: List[str]
    date: datetime
    for_: Optional[List[str]]
    from_: Optional[List[str]]
    src: str
    with_: str
    delay: int

    class Config:
        fields = {"with_": "with", "for_": "for", "from_": "from"}


class Header(APIModel):
    message_id: Optional[str]
    subject: str
    defect: Optional[List[str]]
    from_: str
    to: List[str]
    cc: Optional[List[str]]
    date: Optional[datetime]
    received_email: Optional[List[str]]
    received_foremail: Optional[List[str]]
    received_domain: Optional[List[str]]
    received_ip: Optional[List[str]]
    received_src: Optional[str]
    received: List[Received]
    header: Dict[str, List[Union[str, int]]]

    class Config:
        fields = {"from_": "from"}


class Eml(APIModel):
    attachments: List[Attachment]
    bodies: List[Body]
    header: Header

    class Config:
        fields = {"hash_": "hash"}
