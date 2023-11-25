from humps import camelize
from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=camelize, populate_by_name=True
    )
