import pytest

from backend.schemas.payload import FilePayload


def test_sample_eml(sample_eml: bytes):
    assert FilePayload(file=sample_eml) is not None


def test_multipart_eml(multipart_eml: bytes):
    assert FilePayload(file=multipart_eml) is not None


def test_encrypted_docx_eml(encrypted_docx_eml: bytes):
    assert FilePayload(file=encrypted_docx_eml) is not None


def test_cc_eml(cc_eml: bytes):
    assert FilePayload(file=cc_eml) is not None


def test_invalid_eml_file():
    with pytest.raises(ValueError):
        FilePayload(file=b"")
