import app.repositories.film_repository as film_repo
from app.exceptions.film import FilmNotFound,FilmsNotFound


async def get_film(customer_id:int,conn):

    film = await film_repo.get_film(customer_id,conn)

    if not film:
        raise FilmNotFound

    return {
            "film_id":film[0],
            "title":film[1],
            "release_year":film[2],
            "length":film[3],
            "rating":film[4]
    
        }


async def get_films(page:int | None ,limit:int | None ,conn):

    if page != None:

        if page < 0:
            raise ValueError
        
        if limit is None:
            limit = 10
        
        offset = (page - 1) * limit

    else:
        offset = page

    if limit and limit < 0:
        raise ValueError

    films =  await film_repo.get_films(offset,limit,conn)

    if not films:
        raise FilmsNotFound


    return [
            {
                "film_id":film[0],
                "title":film[1],
                "release_year":film[2],
                "length":film[3],
                "rating":film[4]
            } for film in films
        ]


async def search_by_title(film_title:str,conn):
    film_title = film_title.title()
    film =  await film_repo.search_by_title(film_title,conn)

    if not film:
        raise FilmNotFound

    return {
            "film_id":film[0],
            "title":film[1],
            "release_year":film[2],
            "length":film[3],
            "rating":film[4]
    
        }

