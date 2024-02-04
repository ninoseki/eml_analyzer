from urllib.parse import urlparse

import httpx
from starlette.datastructures import Secret

from backend import schemas


class UrlScan(httpx.AsyncClient):
    def __init__(self, api_key: Secret) -> None:
        super().__init__(
            base_url="https://urlscan.io", headers={"api-key": str(api_key)}
        )

    async def lookup(
        self,
        url: str,
    ) -> schemas.UrlScanLookup:
        parsed = urlparse(url)
        params = {
            "q": f'task.url:"{url}" AND task.domain:"{parsed.hostname}" AND verdicts.malicious:true',
            "size": 1,
        }
        r = await self.get("/api/v1/search/", params=params)
        r.raise_for_status()
        return schemas.UrlScanLookup.model_validate(r.json())
