import io

# Own modules
from rtfparse import re_patterns, utils
from rtfparse.entities import CONTROL_WORD, INTEGER_MAGNITUDE, Entity, logger


class Control_Word(Entity):  # noqa: N801
    def __init__(self, encoding: str, file: io.BufferedReader) -> None:
        super().__init__()
        self.encoding = encoding
        logger.debug(f"Reading Control Word at file position {file.tell()}")
        self.control_name = "missing"
        self.parameter = ""
        self.bindata = b""
        self.start_position = file.tell()
        logger.debug(f"Starting at file position {self.start_position}")
        probe = file.read(CONTROL_WORD)
        if match := re_patterns.control_word.match(probe):
            self.control_name = match.group("control_name").decode(self.encoding)
            logger.debug(f"Preliminary {self.control_name = }")
            parameter = match.group("parameter")
            if parameter is not None:
                self.parameter = int(parameter.decode(self.encoding))
                logger.debug(f"{self.parameter = }")
                self.control_name = self.control_name.removesuffix(str(self.parameter))
                logger.debug(f"Final {self.control_name = }")
            target_position = self.start_position + match.span()[1]
            if match.group("other"):
                logger.debug(
                    f"Delimiter is {match.group('other').decode(self.encoding)}, len: {len(match.group('delimiter'))}"
                )
                target_position -= len(match.group("delimiter"))
            file.seek(target_position)
            # handle \binN:
            if self.control_name == "bin":
                self.bindata = file.read(
                    utils.twos_complement(self.parameter, INTEGER_MAGNITUDE)
                )
        else:
            logger.warning("Missing Control Word")
            # file.seek(target_position)
