import os

import aiospamc
import ci
import pytest
from fastapi.testclient import TestClient
from pytest_docker.plugin import Services
from syncer import sync

from backend import clients, factories, schemas
from backend.main import create_app


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "test.docker-compose.yml")


@sync
async def is_spam_assassin_responsive(port: int) -> bool:
    try:
        res = await aiospamc.ping(port=port)
        return res is not None
    except Exception:
        return False


if ci.is_ci():

    @pytest.fixture(scope="session", autouse=True)
    def docker_compose():  # type: ignore
        return
else:

    @pytest.fixture(scope="session", autouse=True)
    def docker_compose(docker_ip: str, docker_services: Services):
        port = docker_services.port_for("spamassassin", 783)
        docker_services.wait_until_responsive(
            timeout=60.0, pause=0.1, check=lambda: is_spam_assassin_responsive(port)
        )


@pytest.fixture
def spam_assassin() -> clients.SpamAssassin:
    return clients.SpamAssassin()


@pytest.fixture
def sample_eml() -> bytes:
    with open("tests/fixtures/sample.eml", "rb") as f:
        return f.read()


@pytest.fixture
def cc_eml() -> bytes:
    with open("tests/fixtures/cc.eml", "rb") as f:
        return f.read()


@pytest.fixture
def multipart_eml() -> bytes:
    with open("tests/fixtures/multipart.eml", "rb") as f:
        return f.read()


@pytest.fixture
def encrypted_docx_eml() -> bytes:
    with open("tests/fixtures/encrypted_docx.eml", "rb") as f:
        return f.read()


@pytest.fixture
def content_id_eml() -> bytes:
    with open("tests/fixtures/content_id.eml", "rb") as f:
        return f.read()


@pytest.fixture
def outer_msg() -> bytes:
    with open("tests/fixtures/outer.msg", "rb") as f:
        return f.read()


@pytest.fixture
def other_msg() -> bytes:
    with open("tests/fixtures/other.msg", "rb") as f:
        return f.read()


@pytest.fixture
def encrypted_docx() -> bytes:
    with open("tests/fixtures/encrypted.docx", "rb") as f:
        return f.read()


@pytest.fixture
def xls_with_macro() -> bytes:
    with open("tests/fixtures/macro.xls", "rb") as f:
        return f.read()


@pytest.fixture
def complete_msg() -> bytes:
    with open("tests/fixtures/complete.msg", "rb") as f:
        return f.read()


@pytest.fixture
def test_html() -> str:
    with open("tests/fixtures/test.html") as f:
        return f.read()


@pytest.fixture
def dkim_valid_eml() -> bytes:
    with open("tests/fixtures/emails/dkim/valid.eml", "rb") as f:
        return f.read()


@pytest.fixture
def dkim_invalid_eml() -> bytes:
    with open("tests/fixtures/emails/invalid.eml", "rb") as f:
        return f.read()


@pytest.fixture
def dkim_no_signature_eml() -> bytes:
    with open("tests/fixtures/emails/dkim/no_signature.eml", "rb") as f:
        return f.read()


@pytest.fixture
def docx_attachment(encrypted_docx_eml: bytes) -> schemas.Attachment:
    eml = factories.EmlFactory().call(encrypted_docx_eml)
    return eml.attachments[0]


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
