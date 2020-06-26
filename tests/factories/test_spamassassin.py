from app.factories.spamassassin import SpamAssassinVerdictFactory


def test_encrypted_docx(encrypted_docx_eml):
    verdict = SpamAssassinVerdictFactory.from_bytes(encrypted_docx_eml)
    assert verdict.malicious is False
    assert len(verdict.details) > 0


def test_sample(sample_eml):
    verdict = SpamAssassinVerdictFactory.from_bytes(sample_eml)
    assert verdict.malicious is False
    assert len(verdict.details) > 0
