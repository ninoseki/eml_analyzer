from app.core.resources import httpx_client
from app.schemas.emailrep import EmailRepResponse


class EmailRep:
    HOST = "emailrep.io"
    BASE_URL = f"https://{HOST}"

    def __init__(self, client=httpx_client):
        self.client = httpx_client

    async def get(self, email: str) -> EmailRepResponse:
        url = f"{self.BASE_URL}/{email}"
        r = await self.client.get(url)
        r.raise_for_status()
        return EmailRepResponse.parse_obj(r.json())
