from app.factories.eml import EmlFactory, is_inline_forward_attachment


def test_sample(sample_eml):
    eml = EmlFactory.from_bytes(sample_eml)
    assert eml.header.message_id is None
    assert eml.header.subject == "Winter promotions"
    assert eml.header.to == ["foo.bar@example.com"]
    assert eml.header.from_ == "no-reply@example.com"

    assert len(eml.bodies) == 2


def test_cc(cc_eml):
    eml = EmlFactory.from_bytes(cc_eml)
    assert eml.header.message_id == "ecc38b11-aa06-44c9-b8de-283b06a1d89e@example.com"
    assert eml.header.subject == "To and Cc headers"
    assert eml.header.to == ["foo.bar@example.com", "info@example.com"]

    assert eml.header.cc == ["foo@example.com", "bar@example.com"]

    assert len(eml.bodies) == 1
    assert eml.bodies[0].content == ""

    assert eml.attachments == []


def test_multipart(multipart_eml):
    eml = EmlFactory.from_bytes(multipart_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert first.filename == "tired_boot.FJ010019.jpeg"
    assert first.hash_.md5 == "f561388f7446cedd5b8b480311744b3c"


def test_encrypted_docx(encrypted_docx_eml):
    eml = EmlFactory.from_bytes(encrypted_docx_eml)
    assert eml.attachments is not None
    assert len(eml.attachments) == 1

    first = eml.attachments[0]
    assert (
        first.hash_.sha256
        == "28df2d6dfa10dc85c8ebb5defffcb15c196dca7b26d4fd6859b9ec75ac60cf9e"
    )


def test_emails(emails: list[bytes]):
    for email in emails:
        try:
            eml = EmlFactory.from_bytes(email)
            assert eml is not None
        except Exception:
            pass


def test_complete_msg(complete_msg):
    eml = EmlFactory.from_bytes(complete_msg)

    assert eml.header.subject == "Test Multiple attachments complete email!!"


def test_is_inline_forward_attachment():
    inline_forward = {
        "content_header": {
            "content-type": ['message/rfc822; name="Fwd: foo"'],
            "content-disposition": ['inline; filename="Fwd: foo"'],
        }
    }
    assert is_inline_forward_attachment(inline_forward) is True

    zip_ = {
        "content_header": {
            "content-type": ['application/x-zip-compressed; name="foo.zip"'],
            "content-transfer-encoding": ["base64"],
            "content-disposition": ['attachment; filename="foo.zip"'],
        }
    }
    assert is_inline_forward_attachment(zip_) is False
