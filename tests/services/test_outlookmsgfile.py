from io import BytesIO

from backend.services.outlookmsgfile import Message


def test_other_msg(other_msg: bytes):
    file = BytesIO(other_msg)
    message = Message(file)
    email = message.to_email()

    assert email["Subject"] == "投递状态通知 (Failure Notice)"
    assert email["To"] == "yosipnps@model.com"

    attachments = list(email.iter_attachments())
    assert len(attachments) == 1


def test_outer_msg(outer_msg: bytes):
    file = BytesIO(outer_msg)
    message = Message(file)
    email = message.to_email()

    assert email["Subject"] == "outer subject"
    assert email["To"] == "outer@foo.bar"

    attachments = list(email.iter_attachments())
    assert len(attachments) == 1
