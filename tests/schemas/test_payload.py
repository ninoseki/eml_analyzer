import pytest

from app.schemas.payload import FilePayload


def test_sample_eml(sample_eml: bytes):
    FilePayload(file=sample_eml)


def test_multipart_eml(multipart_eml: bytes):
    FilePayload(file=multipart_eml)


def test_encrypted_docx_eml(encrypted_docx_eml: bytes):
    FilePayload(file=encrypted_docx_eml)


def test_cc_eml(cc_eml: bytes):
    FilePayload(file=cc_eml)


def test_invalid_eml_file():
    with pytest.raises(ValueError):
        FilePayload(file=b"")
