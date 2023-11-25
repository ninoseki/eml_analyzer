from backend.factories.eml import EmlFactory
from backend.factories.oldid import OleIDVerdictFactory
from backend.schemas.eml import Attachment


def get_attachments(eml_file: bytes) -> list[Attachment]:
    eml = EmlFactory.from_bytes(eml_file)
    return eml.attachments


def test_encrypted_docx(encrypted_docx_eml):
    attachments = get_attachments(encrypted_docx_eml)

    verdict = OleIDVerdictFactory.from_attachments(attachments)
    assert verdict.malicious is True
    assert len(verdict.details) == 1


def test_sample(sample_eml):
    attachments = get_attachments(sample_eml)

    verdict = OleIDVerdictFactory.from_attachments(attachments)
    assert verdict.malicious is False
    assert len(verdict.details) == 1
