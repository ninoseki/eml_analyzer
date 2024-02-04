import io

import httpx
from starlette.datastructures import Secret

from backend import schemas


class InQuest(httpx.AsyncClient):
    def __init__(self, api_key: Secret) -> None:
        super().__init__(
            base_url="https://labs.inquest.net",
            headers={"Authorization": f"Basic: {api_key}"},
        )

    async def lookup(self, sha256: str) -> schemas.InQuestLookup:
        r = await self.get("/api/dfi/details", params={"sha256": sha256})
        r.raise_for_status()
        return schemas.InQuestLookup.model_validate(r.json())

    async def submit(self, f: io.BytesIO) -> schemas.SubmissionResult:
        r = await self.post("/api/dfi/upload", files={"file": f})
        r.raise_for_status()
        data = r.json()["data"]
        return schemas.SubmissionResult(
            reference_url=f"https://labs.inquest.net/dfi/sha256/{data}"
        )
