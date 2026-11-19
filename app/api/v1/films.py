from fastapi import APIRouter,HTTPException,Depends,Query
from fastapi.security import OAuth2PasswordBearer

from ..dependencies import get_db
from app.schemas.films import FilmResponse,TitleSearch
import app.services.film_services as film_services
from app.services.user_services import get_current_user,user_rate_limit


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

router = APIRouter(
    prefix="/films",
    tags=["Films"]
)


@router.get("/{film_id}",response_model=FilmResponse,
            dependencies=[Depends(user_rate_limit(10,60000))])
async def get_film(film_id:int,conn=Depends(get_db),
                   current_user=Depends(get_current_user)):

    return await film_services.get_film(film_id,conn)



@router.get("",response_model=list[FilmResponse],
            dependencies=[Depends(user_rate_limit(10,60000))])
async def get_films(page:int | None =None,
                    limit:int | None = None,
                    conn = Depends(get_db),
                    current_user=Depends(get_current_user)):

    return await film_services.get_films(page,limit,conn)


@router.get("/search/",response_model=FilmResponse,
            dependencies=[Depends(user_rate_limit(10,60000))])
async def search_by_title(film_title:TitleSearch = Query(),conn = Depends(get_db),
                          current_user=Depends(get_current_user)):


    return await film_services.search_by_title(film_title.title,conn)
    