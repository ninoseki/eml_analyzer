from pydantic import BaseModel, Field


class Verdicts(BaseModel):
    score: int
    malicious: bool


class Page(BaseModel):
    url: str


Task = Page


class Result(BaseModel):
    page: Page
    task: Task
    verdicts: Verdicts
    result: str

    @property
    def link(self):
        return self.result.replace("/api/v1/", "")


class UrlScanLookup(BaseModel):
    results: list[Result] = Field(default_factory=list)
