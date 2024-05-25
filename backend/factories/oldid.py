import base64
import itertools

from returns.result import safe

from backend import schemas
from backend.oleid import OleID

from .abstract import AbstractFactory


@safe
def parse(attachment: schemas.Attachment) -> OleID:
    data: bytes = base64.b64decode(attachment.raw)
    return OleID(data)


@safe
def attachment_to_details(
    attachment: schemas.Attachment,
) -> list[schemas.VerdictDetail]:
    details: list[schemas.VerdictDetail] = []
    file_info = f"{attachment.filename}({attachment.hash.sha256})"

    def inner(oleid: OleID):
        if oleid.has_vba_macros:
            details.append(
                schemas.VerdictDetail(
                    key="vba", description=f"{file_info} contains VBA macros."
                )
            )

        if oleid.has_xlm_macros:
            details.append(
                schemas.VerdictDetail(
                    key="xlm", description=f"{file_info} contains XLM macros."
                )
            )

        if oleid.has_flash_objects:
            details.append(
                schemas.VerdictDetail(
                    key="flash", description=f"{file_info} contains Flash objects."
                )
            )

        if oleid.has_encrypted:
            details.append(
                schemas.VerdictDetail(
                    key="encrypted", description=f"{file_info} is encrypted."
                )
            )

        if oleid.has_external_relationships:
            details.append(
                schemas.VerdictDetail(
                    key="ext_rels",
                    description=f"{file_info} contains external relationships.",
                )
            )

        if oleid.has_object_pool:
            details.append(
                schemas.VerdictDetail(
                    key="ObjectPool",
                    description=f"{file_info} contains an ObjectPool stream.",
                )
            )

    parse(attachment).map(inner)
    return details


class OleIDVerdictFactory(AbstractFactory):
    def __init__(self, name: str = "oleid"):
        self.name = name

    def call(
        self,
        attachments: list[schemas.Attachment],
    ) -> schemas.Verdict:
        details = list(
            itertools.chain.from_iterable(
                [
                    attachment_to_details(attachment).value_or([])
                    for attachment in attachments
                ]
            )
        )

        malicious = len(details) > 0
        if not malicious:
            details.append(
                schemas.VerdictDetail(
                    key="benign",
                    description="There is no suspicious OLE file in attachments.",
                )
            )
        return schemas.Verdict(name=self.name, malicious=malicious, details=details)
