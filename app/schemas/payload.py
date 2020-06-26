from fastapi_utils.api_model import APIModel


class Payload(APIModel):
    eml_file: str
