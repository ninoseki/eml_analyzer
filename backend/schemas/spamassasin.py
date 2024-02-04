from pydantic import BaseModel, Field


class SpamAssassinDetail(BaseModel):
    name: str
    score: float
    description: str


class SpamAssassinReport(BaseModel):
    score: float
    details: list[SpamAssassinDetail] = Field(default_factory=list)

    def is_spam(self, level: float = 5.0) -> bool:
        return self.score is None or self.score > level
