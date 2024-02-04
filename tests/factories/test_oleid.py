from backend import factories, schemas


def get_attachments(eml_file: bytes) -> list[schemas.Attachment]:
    eml = factories.EmlFactory.call(eml_file)
    return eml.attachments


def test_encrypted_docx(encrypted_docx_eml: bytes):
    verdict = factories.OleIDVerdictFactory.call(get_attachments(encrypted_docx_eml))
    assert verdict.malicious is True
    assert len(verdict.details) == 1


def test_sample(sample_eml: bytes):
    verdict = factories.OleIDVerdictFactory.call(get_attachments(sample_eml))
    assert verdict.malicious is False
    assert len(verdict.details) == 1
