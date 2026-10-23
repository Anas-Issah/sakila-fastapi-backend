from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CustomerResponse(BaseModel):
    customer_id:int
    customer_first_name:str
    customer_last_name:str
    customer_email:str


class CustomerNotFound(BaseModel):
    error:str
    detail:str

class CustomerSearch(BaseModel):
    first_name: Optional[str] = None
    last_name:  Optional[str] = None


    @field_validator("first_name","last_name")
    @classmethod
    def name_can_not_be_blank(cls, value: Optional[str] )-> Optional[str]:

        if value is None:
            return None

        if not value.strip():
            raise ValueError(f"{value} can not be whitespace")

        return value