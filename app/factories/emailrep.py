from loguru import logger

from app.schemas.verdict import Detail, Verdict
from app.services.emailrep import EmailRep


class EmailRepVerdictFactory:
    def __init__(self, email: str):
        self.email = email
        self.name = "EmailRep"

    async def to_model(self) -> Verdict:
        details: list[Detail] = []
        malicious = False

        email_rep = EmailRep()
        try:
            res = await email_rep.get(self.email)
            if res.suspicious is True:
                malicious = True
                description = f"{self.email} is suspicious. See https://emailrep.io/{self.email} for details."
                details.append(Detail(key="EmailRep", description=description))
            else:
                description = f"{self.email} is not suspicious. See https://emailrep.io/{self.email} for details."
                details.append(Detail(key="EmailRep", description=description))
        except Exception as error:
            logger.error(error)

        return Verdict(name=self.name, malicious=malicious, details=details)

    @classmethod
    async def from_email(cls, email) -> Verdict:
        obj = cls(email)
        return await obj.to_model()
