import httpx
from fastapi import APIRouter, HTTPException, status

from backend import dependencies, schemas
from backend.schemas.eml import Attachment
from backend.utils import attachment_to_file

router = APIRouter()


@router.post(
    "/virustotal",
    response_description="Return a submission result",
    summary="Submit an attachment to VirusTotal",
    description="Submit an attachment to VirusTotal",
    status_code=200,
)
async def submit_to_virustotal(
    attachment: Attachment, *, optional_vt: dependencies.OptionalVirusTotal
) -> schemas.SubmissionResult:
    if optional_vt is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the VirusTotal API key",
        )

    try:
        await optional_vt.scan_file_async(attachment_to_file(attachment))
        sha256 = attachment.hash.sha256
        return schemas.SubmissionResult(
            reference_url=f"https://www.virustotal.com/gui/file/{sha256}/detection"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Something went wrong with VirusTotal submission: {e}",
        ) from e
