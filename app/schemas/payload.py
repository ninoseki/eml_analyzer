from fastapi_utils.api_model import APIModel
from pydantic import validator

from app.services.validator import is_eml_or_msg_file


class Payload(APIModel):
    file: str


class FilePayload(APIModel):
    file: bytes

    @validator("file")
    def eml_file_must_be_eml(cls, v: bytes):
        if not is_eml_or_msg_file(v):
            raise ValueError("Invalid file format.")
        return v
