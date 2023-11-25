from fastapi import APIRouter, HTTPException, status
from httpx._exceptions import HTTPError

from backend.core.utils import has_inquest_api_key, has_virustotal_api_key
from backend.schemas.eml import Attachment
from backend.schemas.submission import SubmissionResult
from backend.submitters.inquest import InQuestSubmitter
from backend.submitters.virustotal import VirusTotalSubmitter

router = APIRouter()


@router.post(
    "/inquest",
    response_description="Return a submission result",
    summary="Submit an attachment to InQuest",
    description="Submit an attachment to InQuest",
    status_code=200,
)
async def submit_to_inquest(attachment: Attachment) -> SubmissionResult:
    if not has_inquest_api_key():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the InQuest API key",
        )
    # check ext type
    valid_types = ["doc", "docx", "ppt", "pptx", "xls", "xlsx"]
    if attachment.extension not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"{attachment.extension} is not supported.",
        )

    submitter = InQuestSubmitter(attachment)
    try:
        return await submitter.submit()
    except HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong with InQuest submission: {e!s}",
        ) from e


@router.post(
    "/virustotal",
    response_model=SubmissionResult,
    response_description="Return a submission result",
    summary="Submit an attachment to VirusTotal",
    description="Submit an attachment to VirusTotal",
    status_code=200,
)
async def submit_to_virustotal(attachment: Attachment) -> SubmissionResult:
    if not has_virustotal_api_key():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the VirusTotal API key",
        )

    submitter = VirusTotalSubmitter(attachment)
    try:
        return await submitter.submit()
    except HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong with VirusTotal submission: {e!s}",
        ) from e
