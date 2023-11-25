from typing import cast

import magic

EML_MIME_TYPES = ["message/rfc822", "text/html", "text/plain"]
MSG_MIME_TYPES = ["application/vnd.ms-outlook"]


def check_mime_type(data: bytes, valid_types: list[str]) -> bool:
    detected = magic.detect_from_content(data)
    mime_type = cast(str, detected.mime_type)

    if mime_type in valid_types:
        return True

    return False


def is_eml_or_msg_file(data: bytes):
    valid_types = EML_MIME_TYPES + MSG_MIME_TYPES
    return check_mime_type(data, valid_types)


def is_eml_file(data: bytes) -> bool:
    return check_mime_type(data, EML_MIME_TYPES)


def is_msg_file(data: bytes) -> bool:
    return check_mime_type(data, MSG_MIME_TYPES)
