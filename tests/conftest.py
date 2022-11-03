import glob
from pathlib import Path
from typing import Any

import httpx
import pytest
import pytest_asyncio
from aiospamc.header_values import SpamValue
from aiospamc.responses import Response

from app import create_app
from app.factories.eml import EmlFactory
from app.schemas.eml import Attachment


def read_file(filename) -> str:
    parent = Path(__file__).parent.absolute()
    path = parent / f"fixtures/{filename}"
    with open(path) as f:
        return f.read()


def read_file_as_binary(filename) -> bytes:
    parent = Path(__file__).parent.absolute()
    path = parent / f"fixtures/{filename}"
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture
def sample_eml() -> bytes:
    return read_file("sample.eml").encode()


@pytest.fixture
def cc_eml() -> bytes:
    return read_file("cc.eml").encode()


@pytest.fixture
def multipart_eml() -> bytes:
    return read_file("multipart.eml").encode()


@pytest.fixture
def encrypted_docx_eml() -> bytes:
    return read_file("encrypted_docx.eml").encode()


@pytest.fixture
def emails() -> list[bytes]:
    parent = str(Path(__file__).parent.absolute())
    path = parent + "/fixtures/emails/**/*.eml"
    paths = glob.glob(path)
    return [open(path, "rb").read() for path in paths]


@pytest.fixture
def outer_msg() -> bytes:
    return read_file_as_binary("outer.msg")


@pytest.fixture
def other_msg() -> bytes:
    return read_file_as_binary("other.msg")


@pytest.fixture
def emailrep_response() -> str:
    return read_file("emailrep.json")


@pytest.fixture
def urlscan_search_response() -> str:
    return read_file("urlscan_search.json")


@pytest.fixture
def urlscan_result_response() -> str:
    return read_file("urlscan_result.json")


@pytest.fixture
def inquest_dfi_details_response() -> str:
    return read_file("inquest_dfi_details.json")


@pytest.fixture
def inquest_dfi_upload_response() -> str:
    return read_file("inquest_dfi_upload.json")


@pytest.fixture
def encrypted_docx() -> bytes:
    return read_file_as_binary("encrypted.docx")


@pytest.fixture
def xls_with_macro() -> bytes:
    return read_file_as_binary("macro.xls")


@pytest.fixture
def complete_msg() -> bytes:
    return read_file_as_binary("complete.msg")


@pytest.fixture
def test_html() -> str:
    return read_file("test.html")


@pytest.fixture
def docx_attachment(encrypted_docx_eml: bytes) -> Attachment:
    eml = EmlFactory.from_bytes(encrypted_docx_eml)
    return eml.attachments[0]


@pytest.fixture
def spamassassin_response() -> Response:
    body = read_file("sa.txt").encode()
    headers: dict[str, Any] = {}
    headers["Spam"] = SpamValue(value=True, score=40, threshold=20)
    return Response(headers=headers, body=body)


@pytest_asyncio.fixture
async def client():
    app = create_app()
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as c:
        yield c
