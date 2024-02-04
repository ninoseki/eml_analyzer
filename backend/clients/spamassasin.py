import aiospamc
from aiospamc.header_values import Headers
from async_timeout import timeout

from backend import schemas, settings


class Parser:
    def __init__(self, headers: Headers, body: str):
        self.headers = headers
        self.body = body
        self.score = 0.0
        self.details: list[schemas.SpamAssassinDetail] = []

    def _parse_headers(self):
        spam_value = self.headers.get("Spam")
        if spam_value is not None:
            self.score = spam_value.score

    def _parse_detail(self, line: str) -> schemas.SpamAssassinDetail:
        parts = line.split()
        score = float(parts[0])
        name = parts[1]
        description = " ".join(parts[2:])
        return schemas.SpamAssassinDetail(
            name=name, score=score, description=description
        )

    def _parse_details(self, details: str) -> list[schemas.SpamAssassinDetail]:
        lines = details.splitlines()
        normalized_line: list[str] = []

        for line in lines:
            parts = line.split()
            first_char = parts[0][0]
            if first_char.isnumeric() or first_char == "-":
                normalized_line.append(line)
            else:
                normalized_line[-1] += f" {line}"

        return [self._parse_detail(line) for line in normalized_line]

    def _parse_body(self):
        lines = [line for line in self.body.splitlines() if line != ""]
        delimiter_index = 0
        for index, line in enumerate(lines):
            if "---" in line:
                delimiter_index = index + 1
                break

        details = "\n".join(lines[delimiter_index:])
        self.details = self._parse_details(details)

    def parse(self) -> schemas.SpamAssassinReport:
        self._parse_headers()
        self._parse_body()
        return schemas.SpamAssassinReport(score=self.score, details=self.details)


class SpamAssassin:
    def __init__(
        self,
        host: str = settings.SPAMASSASSIN_HOST,
        port: int = settings.SPAMASSASSIN_PORT,
        timeout: int = settings.SPAMASSASSIN_TIMEOUT,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout

    async def report(self, message: bytes) -> schemas.SpamAssassinReport:
        async with timeout(self.timeout):
            response = await aiospamc.report(message, host=self.host, port=self.port)

        parser = Parser(headers=response.headers, body=response.body.decode())
        return parser.parse()
