from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx._exceptions import HTTPError

from app.core.utils import has_inquest_api_key, has_virustotal_api_key
from app.schemas.eml import Attachment
from app.schemas.submission import SubmissionResult
from app.submitters.inquest import InQuestSubmitter
from app.submitters.virustotal import VirusTotalSubmitter

router = APIRouter()


@router.post(
    "/inquest",
    response_model=SubmissionResult,
    response_description="Return a submission result",
    summary="Submit an attachment to InQuest",
    description="Submit an attachment to InQuest",
    status_code=200,
)
async def submit_to_inquest(attachment: Attachment) -> SubmissionResult:
    if not has_inquest_api_key():
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder({"detail": "You don't have the InQuest API key"}),
        )

    submitter = InQuestSubmitter(attachment)
    try:
        return await submitter.submit()
    except HTTPError as e:
        detail = f"Something went wrong with InQuest submission: {str(e)}"
        return JSONResponse(
            status_code=500, content=jsonable_encoder({"detail": detail})
        )


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
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder(
                {"detail": "You don't have the VirusTotal API key"}
            ),
        )

    submitter = VirusTotalSubmitter(attachment)
    try:
        return await submitter.submit()
    except HTTPError as e:
        detail = f"Something went wrong with VirusTotal submission: {str(e)}"
        return JSONResponse(
            status_code=500, content=jsonable_encoder({"detail": detail})
        )
