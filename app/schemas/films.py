from pydantic import BaseModel,field_validator

from exceptions.film import FilmTitleError

class FilmResponse(BaseModel):
    film_id:int
    title:str
    release_year:int 
    length:int 
    rating:str

class TitleSearch(BaseModel):
    title:str 

    @field_validator("title")
    @classmethod
    def validate_film_title(cls,value:str ):

        if  not value.strip():
            raise FilmTitleError

        return value

    