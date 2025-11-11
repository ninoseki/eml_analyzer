from pathlib import Path

import pytest

from backend import factories
from backend.factories.eml import is_inline_forward_attachment


@pytest.fixture()
def factory():
    return factories.EmlFactory()


def test_sample(sample_eml: bytes, factory: factories.EmlFactory):
    eml = factory.call(sample_eml)
    assert eml.header.message_id is None
    assert eml.header.subject == "Winter promotions"
    assert eml.header.to == ["foo.bar@example.com"]
    assert eml.header.from_ == "no-reply@example.com"

    assert len(eml.bodies) == 2


def test_cc(cc_eml: bytes, factory: factories.EmlFactory):
    eml = factory.call(cc_eml)
    assert eml.header.message_id == "<ecc38b11-aa06-44c9-b8de-283b06a1d89e@example.com>"
    assert eml.header.subject == "To and Cc headers"
    assert eml.header.to == ["foo.bar@example.com", "info@example.com"]

    assert eml.header.cc == ["foo@example.com", "bar@example.com"]

    assert len(eml.bodies) == 1
    assert eml.bodies[0].content == ""

    assert eml.attachments == []


def test_multipart(multipart_eml: bytes, factory: factories.EmlFactory):
    eml = factory.call(multipart_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert first.filename == "tired_boot.FJ010019.jpeg"
    assert first.hash.md5 == "f561388f7446cedd5b8b480311744b3c"


def test_encrypted_docx(encrypted_docx_eml: bytes, factory: factories.EmlFactory):
    eml = factory.call(encrypted_docx_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert (
        first.hash.sha256
        == "28df2d6dfa10dc85c8ebb5defffcb15c196dca7b26d4fd6859b9ec75ac60cf9e"
    )


def test_content_id(content_id_eml: bytes, factory: factories.EmlFactory):
    eml = factory.call(content_id_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert first.content_id == "<id42@guppylake.bellcore.com>"


def test_email(factory: factories.EmlFactory, subtests: pytest.Subtests):
    email_dir = Path("tests/fixtures/emails")
    for path in email_dir.glob("**/*.eml"):
        with subtests.test(path=path):
            assert factory.call(path.read_bytes()) is not None


def test_complete_msg(complete_msg: bytes, factory: factories.EmlFactory):
    eml = factory.call(complete_msg)
    assert eml.header.subject == "Test Multiple attachments complete email!!"


@pytest.mark.parametrize(
    "attachment,expected",
    [
        (
            {
                "content_header": {
                    "content-type": ['message/rfc822; name="Fwd: foo"'],
                    "content-disposition": ['inline; filename="Fwd: foo"'],
                }
            },
            True,
        ),
        (
            {
                "content_header": {
                    "content-type": ['application/x-zip-compressed; name="foo.zip"'],
                    "content-transfer-encoding": ["base64"],
                    "content-disposition": ['attachment; filename="foo.zip"'],
                }
            },
            False,
        ),
    ],
)
def test_is_inline_forward_attachment(attachment: dict, expected: bool):
    assert is_inline_forward_attachment(attachment) is expected


@pytest.fixture
def invalid_datetime_eml() -> bytes:
    with open("tests/fixtures/invalid_datetime.eml", "rb") as f:
        return f.read()


def test_invalid_datetime(factory: factories.EmlFactory, invalid_datetime_eml: bytes):
    eml = factory.call(invalid_datetime_eml)
    assert isinstance(eml.header.received[0].date, str)
    # delay should be None because the base datetime (= header.received[0].date) is invalid
    for r in eml.header.received:
        assert r.delay is None
