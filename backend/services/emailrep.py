from backend.core.resources import httpx_client
from backend.schemas.emailrep import EmailRepResponse


class EmailRep:
    HOST = "emailrep.io"
    BASE_URL = f"https://{HOST}"

    def __init__(self, client=httpx_client):
        self.client = httpx_client

    async def get(self, email: str) -> EmailRepResponse:
        url = f"{self.BASE_URL}/{email}"
        r = await self.client.get(url)
        r.raise_for_status()
        return EmailRepResponse.model_validate(r.json())
