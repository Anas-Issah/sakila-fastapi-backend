from pydantic import BaseModel,field_validator

from exceptions.users import UsernamePasswordValueError

class NewUser(BaseModel):
    username:str
    password:str

    @field_validator("username","password")
    @classmethod
    def validator(cls,value:str) -> str:

        if not value or (not value.strip()):
            raise UsernamePasswordValueError

        return value
    