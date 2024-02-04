from pydantic import field_validator

from backend.validator import is_eml_or_msg_file

from .api_model import APIModel


class Payload(APIModel):
    file: str


class FilePayload(APIModel):
    file: bytes

    @field_validator("file")
    @classmethod
    def eml_file_must_be_eml(cls, v: bytes):
        if not is_eml_or_msg_file(v):
            raise ValueError("Invalid file format.")
        return v
