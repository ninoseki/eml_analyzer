from io import BytesIO
from typing import cast

from httpx._client import AsyncClient
from httpx._exceptions import HTTPError

from backend.core.resources import httpx_client
from backend.core.settings import INQUEST_API_KEY


class InQuest:
    HOST = "labs.inquest.net"
    BASE_URL = f"https://{HOST}/api"

    def __init__(
        self, client: AsyncClient = httpx_client, api_key: str = str(INQUEST_API_KEY)
    ):
        self.client = client
        self.api_key = api_key

    def _url_for(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"

    def _headers(self) -> dict:
        return {"Authorization": f"Basic: {self.api_key}"}

    async def dfi_details(self, sha256: str) -> dict | None:
        try:
            r = await self.client.get(
                self._url_for("/dfi/details"),
                params={"sha256": sha256},
                headers=self._headers(),
            )
            r.raise_for_status()
            return cast(dict, r.json())
        except HTTPError:
            return None

    async def dfi_upload(self, file_: BytesIO) -> dict:
        files = {"file": file_}

        r = await self.client.post(
            self._url_for("/dfi/upload"),
            files=files,
            headers=self._headers(),
        )
        r.raise_for_status()
        return cast(dict, r.json())
