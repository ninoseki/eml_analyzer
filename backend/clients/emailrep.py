import httpx
from starlette.datastructures import Secret

from backend import schemas


class EmailRep(httpx.AsyncClient):
    def __init__(self, api_key: Secret) -> None:
        super().__init__(
            base_url="https://emailrep.io",
            headers={"key": str(api_key), "user-agent": "EML-Analyzer"},
        )

    async def lookup(self, email: str) -> schemas.EmailRepLookup:
        r = await self.get(f"/{email}")
        r.raise_for_status()
        return schemas.EmailRepLookup.model_validate(r.json())
