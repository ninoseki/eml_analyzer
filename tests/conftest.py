from pathlib import Path

import httpx
import pytest

from app import create_app


def read_eml(filename) -> str:
    parent = Path(__file__).parent.absolute()
    path = parent / f"fixtures/{filename}"
    with open(path) as f:
        return f.read()


@pytest.fixture
def sample_eml() -> bytes:
    return read_eml("sample.eml").encode()


@pytest.fixture
def cc_eml() -> bytes:
    return read_eml("cc.eml").encode()


@pytest.fixture
def multipart_eml() -> bytes:
    return read_eml("multipart.eml").encode()


@pytest.fixture
def encrypted_docx_eml() -> bytes:
    return read_eml("encrypted_docx.eml").encode()


@pytest.fixture
def client():
    app = create_app()
    return httpx.AsyncClient(app=app, base_url="http://testserver")
