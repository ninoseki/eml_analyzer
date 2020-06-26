# Forked from https://github.com/petermat/spamassassin_client
import re
import select
import socket
from io import BytesIO
from typing import Any, Dict, Optional, cast

from loguru import logger

divider_pattern = re.compile(br"^(.*?)\r?\n(.*?)\r?\n\r?\n", re.DOTALL)
first_line_pattern = re.compile(br"^SPAMD/[^ ]+ 0 EX_OK$")


class SpamAssassin:
    def __init__(self, message: bytes, host="127.0.0.1", port=783, timeout=20):
        self.score: Optional[float] = None
        self.symbols = None

        # Connecting
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((host, port))

        # Sending
        client.sendall(self._build_message(message))
        client.shutdown(socket.SHUT_WR)

        # Reading
        resfp = BytesIO()
        while True:
            ready = select.select([client], [], [], timeout)
            if ready[0] is None:
                # Kill with Timeout!
                logger.info("[SpamAssassin] - Timeout ({}s)!".format(str(timeout)))
                break

            data = client.recv(4096)
            if data == b"":
                break

            resfp.write(data)

        # Closing
        client.close()

        self._parse_response(resfp.getvalue())

    def _build_message(self, message: bytes):
        reqfp = BytesIO()
        data_len = str(len(message)).encode()
        reqfp.write(b"REPORT SPAMC/1.2\r\n")
        reqfp.write(b"Content-Length: " + data_len + b"\r\n")
        reqfp.write(b"User: cx42\r\n\r\n")
        reqfp.write(message)
        return reqfp.getvalue()

    def _parse_response(self, response: bytes):
        print(response.decode())
        if response == b"":
            logger.info("[SPAM ASSASSIN] Empty response")
            return None

        match = divider_pattern.match(response)
        if not match:
            logger.error("[SPAM ASSASSIN] Response error:")
            logger.error(response)
            return None

        first_line = match.group(1)
        headers = match.group(2)
        body = response[match.end(0) :]

        # Checking response is good
        match = first_line_pattern.match(first_line)
        if not match:
            logger.error("[SPAM ASSASSIN] invalid response:")
            logger.error(first_line)
            return None

        report_list = [s.strip() for s in body.decode("utf-8").strip().split("\n")]
        linebreak_num = report_list.index([s for s in report_list if "---" in s][0])
        tablelists = [s for s in report_list[linebreak_num + 1 :]]

        self.report_fulltext = "\n".join(report_list)

        # join line when current one is only wrap of previous
        tablelists_temp = []
        if tablelists:
            for counter, tablelist in enumerate(tablelists):
                if len(tablelist) > 1:
                    if (tablelist[0].isnumeric() or tablelist[0] == "-") and (
                        tablelist[1].isnumeric() or tablelist[1] == "."
                    ):
                        tablelists_temp.append(tablelist)
                    else:
                        if tablelists_temp:
                            tablelists_temp[-1] += " " + tablelist
        tablelists = tablelists_temp

        # create final json
        self.report_json = {}
        for tablelist in tablelists:
            wordlist = re.split(r"\s+", tablelist)
            self.report_json[wordlist[1]] = {
                "partscore": float(wordlist[0]),
                "description": " ".join(wordlist[1:]),
            }

        headers = (
            headers.decode("utf-8")
            .replace(" ", "")
            .replace(":", ";")
            .replace("/", ";")
            .split(";")
        )
        self.score = float(headers[2])

    def get_report_json(self) -> Dict[str, Any]:
        return self.report_json

    def get_score(self) -> float:
        return cast(float, self.score)

    def is_spam(self, level=5) -> bool:
        return self.score is None or self.score > level

    def get_fulltext(self) -> str:
        return self.report_fulltext
