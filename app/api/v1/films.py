from fastapi import APIRouter,HTTPException,Depends,Query

from database.connection import get_db
from schemas.films import FilmRespose
import services.film_services as film_services

router = APIRouter(
    prefix="/films",
    tags=["Films"]
)


@router.get("{film_id}",response_model=FilmRespose)
async def get_film(film_id:int,conn=Depends(get_db)):

    return film_services.get_film(film_id,conn)


    


@router.get("",response_model=list[FilmRespose])
async def get_films(page:int | None =None,
                    limit:int | None = None,
                    conn = Depends(get_db)):

    return film_services.get_films(page,limit,conn)
        