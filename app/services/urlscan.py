from typing import Optional, cast

from httpx._exceptions import HTTPError

from app.core.resources import httpx_client
from app.core.settings import URLSCAN_API_KEY


class Urlscan:
    HOST = "urlscan.io"
    VERSION = "v1"
    BASE_URL = f"https://{HOST}/api/{VERSION}"

    def __init__(self, client=httpx_client):
        self.client = httpx_client

    def _url_for(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"

    def _headers(self) -> dict:
        return {"API-Key": str(URLSCAN_API_KEY)}

    async def result(self, uuid: str) -> Optional[dict]:
        try:
            r = await self.client.get(
                self._url_for(f"/result/{uuid}/"), headers=self._headers()
            )
            r.raise_for_status()
            return cast(dict, r.json())
        except HTTPError:
            return None

    async def search(self, url: str, size: int = 10) -> Optional[dict]:
        params = {"q": f'task.url:"{url}"', "size": size}
        try:
            r = await self.client.get(
                self._url_for("/search/"), params=params, headers=self._headers()
            )
            r.raise_for_status()
            return cast(dict, r.json())
        except HTTPError:
            return None
