from pydantic import BaseModel


class CustomerResponse(BaseModel):
    customer_id:int
    customer_first_name:str
    customer_last_name:str
    customer_email:str


class CustomerNotFound(BaseModel):
    error:str
    detail:str