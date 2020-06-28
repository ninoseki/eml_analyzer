from typing import cast

import magic

VALID_MIME_TYPES = ["message/rfc822", "text/html", "text/plain"]


def is_eml_file(data: bytes) -> bool:
    detected = magic.detect_from_content(data)
    mime_type = cast(str, detected.mime_type)

    if mime_type in VALID_MIME_TYPES:
        return True

    return False
