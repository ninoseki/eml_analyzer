from dataclasses import dataclass
from typing import Any

import aiospamc
from async_timeout import timeout


@dataclass
class Detail:
    name: str
    score: float
    description: str


@dataclass
class Report:
    score: float
    details: list[Detail]
    level = 5.0

    def is_spam(self, level: float = 5.0) -> bool:
        return self.score is None or self.score > level


class Parser:
    def __init__(self, headers: dict[str, Any], body: str):
        self.headers = headers
        self.body = body
        self.score = 0.0
        self.details: list[Detail] = []

    def _parse_headers(self):
        spam_value = self.headers["Spam"]
        self.score = spam_value.score

    def _parse_detail(self, line: str) -> Detail:
        parts = line.split()
        score = float(parts[0])
        name = parts[1]
        description = " ".join(parts[2:])
        return Detail(name=name, score=score, description=description)

    def _parse_details(self, details: str) -> list[Detail]:
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
        demiliter_index = 0
        for index, line in enumerate(lines):
            if "---" in line:
                demiliter_index = index + 1
                break

        details = "\n".join(lines[demiliter_index:])
        self.details = self._parse_details(details)

    def parse(self):
        self._parse_headers()
        self._parse_body()

    def to_report(self) -> Report:
        return Report(score=self.score, details=self.details)


class SpamAssassin:
    def __init__(self, host: str = "127.0.0.1", port: int = 783, timeout: int = 10):
        self.host = host
        self.port = port
        self.timeout = timeout

    async def report(self, message: bytes) -> Report:
        async with timeout(self.timeout):
            response = await aiospamc.report(message, host=self.host, port=self.port)

        parser = Parser(headers=response.headers, body=response.body.decode())
        parser.parse()
        return parser.to_report()
