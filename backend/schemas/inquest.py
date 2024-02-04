from pydantic import BaseModel, Field


class InquestAlert(BaseModel):
    category: str
    description: str
    reference: None
    title: str


class Data(BaseModel):
    sha256: str
    classification: str
    inquest_alerts: list[InquestAlert] = Field(default_factory=list)


class InQuestLookup(BaseModel):
    data: Data

    @property
    def malicious(self) -> bool:
        return self.data.classification == "MALICIOUS"

    @property
    def reference_link(self) -> str:
        return f"https://labs.inquest.net/dfi/sha256/{self.data.sha256}"

    @property
    def description(self) -> str:
        malicious_alerts = [
            alert for alert in self.data.inquest_alerts if alert.category == "malicious"
        ]
        descriptions = [alert.description for alert in malicious_alerts]
        return " / ".join(descriptions)
