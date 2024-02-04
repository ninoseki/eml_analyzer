import httpx

from backend import schemas


class EmailRep(httpx.AsyncClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://emailrep.io")

    async def lookup(self, email: str) -> schemas.EmailRepLookup:
        r = await self.get(f"/{email}")
        r.raise_for_status()
        return schemas.EmailRepLookup.model_validate(r.json())
