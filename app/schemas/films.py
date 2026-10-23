from pydantic import BaseModel

class FilmRespose(BaseModel):
    film_id:int
    title:str
    release_year:int 
    length:int 
    rating:str
    