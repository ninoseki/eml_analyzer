import pytest

from backend import factories
from backend.factories.eml import is_inline_forward_attachment


def test_sample(sample_eml: bytes):
    eml = factories.EmlFactory.call(sample_eml)
    assert eml.header.message_id is None
    assert eml.header.subject == "Winter promotions"
    assert eml.header.to == ["foo.bar@example.com"]
    assert eml.header.from_ == "no-reply@example.com"

    assert len(eml.bodies) == 2


def test_cc(cc_eml: bytes):
    eml = factories.EmlFactory.call(cc_eml)
    assert eml.header.message_id == "ecc38b11-aa06-44c9-b8de-283b06a1d89e@example.com"
    assert eml.header.subject == "To and Cc headers"
    assert eml.header.to == ["foo.bar@example.com", "info@example.com"]

    assert eml.header.cc == ["foo@example.com", "bar@example.com"]

    assert len(eml.bodies) == 1
    assert eml.bodies[0].content == ""

    assert eml.attachments == []


def test_multipart(multipart_eml: bytes):
    eml = factories.EmlFactory.call(multipart_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert first.filename == "tired_boot.FJ010019.jpeg"
    assert first.hash.md5 == "f561388f7446cedd5b8b480311744b3c"


def test_encrypted_docx(encrypted_docx_eml: bytes):
    eml = factories.EmlFactory.call(encrypted_docx_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert (
        first.hash.sha256
        == "28df2d6dfa10dc85c8ebb5defffcb15c196dca7b26d4fd6859b9ec75ac60cf9e"
    )


def test_emails(emails: list[bytes]):
    for email in emails:
        eml = factories.EmlFactory.call(email)
        assert eml is not None


def test_complete_msg(complete_msg: bytes):
    eml = factories.EmlFactory.call(complete_msg)
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
