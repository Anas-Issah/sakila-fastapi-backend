from typing import Optional
from pydantic import BaseModel, Field, field_validator

from exceptions.customer import CustomerValueError

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
            raise CustomerValueError

        return value

class NewCustomer(BaseModel):
    store_id:int
    first_name:str
    last_name:str
    email:str
    address_id:int

    @field_validator("first_name","last_name","email")
    @classmethod
    def new_customer_validator(cls,value:str):

        if not value.strip():
            raise CustomerValueError

        return value