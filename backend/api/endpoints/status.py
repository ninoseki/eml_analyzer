from fastapi import APIRouter

from backend import dependencies, schemas

router = APIRouter()


@router.get("/")
async def get_status(
    optional_redis: dependencies.OptionalRedis,
    optional_email_rep: dependencies.OptionalEmailRep,
    optional_inquest: dependencies.OptionalInQuest,
    optional_vt: dependencies.OptionalVirusTotal,
    optional_urlscan: dependencies.OptionalUrlScan,
) -> schemas.Status:
    return schemas.Status(
        cache=optional_redis is not None,
        vt=optional_vt is not None,
        inquest=optional_inquest is not None,
        email_rep=optional_email_rep is not None,
        urlscan=optional_urlscan is not None,
    )
