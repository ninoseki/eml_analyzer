import dkim

from backend import schemas

from .abstract import AbstractAsyncFactory


def transform(is_valid: bool, *, name: str) -> schemas.Verdict:
    """Transform DKIM verification result to Verdict schema."""
    if is_valid:
        details = [
            schemas.VerdictDetail(
                key="dkim_signature",
                description="DKIM signature verified successfully",
            )
        ]
    else:
        details = [
            schemas.VerdictDetail(
                key="dkim_signature",
                description="DKIM signature verification failed or no valid signature found",
            )
        ]

    return schemas.Verdict(
        name=name,
        malicious=not is_valid,
        details=details,
    )


def has_dkim_signature(eml: schemas.Eml) -> bool:
    """Check if the email has a DKIM-Signature header."""
    return any(key.lower() == "dkim-signature" for key in eml.header.header)


class DKIMVerdictFactory(AbstractAsyncFactory):
    def __init__(self, *, name: str = "DKIM"):
        self.name = name

    async def call(
        self,
        eml: schemas.Eml,
        eml_file: bytes,
    ):
        """
        Verify DKIM signature of an email message.

        Args:
            eml_file: Raw email file bytes (can be EML or MSG format)

        Returns:
            Verdict with DKIM verification result
        """
        if not has_dkim_signature(eml):
            return None

        is_valid = await dkim.verify_async(eml_file)
        return transform(is_valid, name=self.name)
