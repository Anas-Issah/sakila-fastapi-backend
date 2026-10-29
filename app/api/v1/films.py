from fastapi import APIRouter,HTTPException,Depends,Query
from fastapi.security import OAuth2PasswordBearer

from database.connection import get_db
from schemas.films import FilmResponse,TitleSearch

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
import services.film_services as film_services
router = APIRouter(
    prefix="/films",
    tags=["Films"]
)


@router.get("{film_id}",response_model=FilmResponse)
async def get_film(film_id:int,conn=Depends(get_db),
                   token:str = Depends(oauth2_scheme)):

    return film_services.get_film(film_id,conn)



@router.get("",response_model=list[FilmResponse])
async def get_films(page:int | None =None,
                    limit:int | None = None,
                    conn = Depends(get_db),
                    token:str = Depends(oauth2_scheme)):

    return film_services.get_films(page,limit,conn)


@router.get("/search/",response_model=FilmResponse)
async def search_by_title(film_title:TitleSearch = Query(),conn = Depends(get_db),
                          token:str = Depends(oauth2_scheme)):


    return film_services.search_by_title(film_title.title,conn)
    