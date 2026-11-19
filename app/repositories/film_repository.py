
async def get_film(film_id:int,conn):
     async with conn.cursor() as cur:
            await cur.execute(
                "SELECT film_id,title,release_year,length,rating " \
                "FROM film " \
                "WHERE film_id = %s",(film_id,)
    
            )
            film = await cur.fetchone()
            return film


async def get_films(offset:int|None,limit:int|None,conn):

    params = []

    query = "SELECT film_id, title, release_year,length,rating " \
                    "FROM film ORDER BY film_id " 

    if offset:
        params.append(offset)
        query = query + " OFFSET %s "

    if limit:
        params.append(limit)
        query = query + "LIMIT %s"
    
    async with conn.cursor() as cur:
        await cur.execute(query,params)

        films = await cur.fetchall()
        return films


async def search_by_title(film_title:str,conn):

    async with conn.cursor() as cur:

        query = "SELECT film_id, title, release_year,length,rating " \
                           "FROM film " \
                           "WHERE title = %s"

        await cur.execute(query,(film_title,))

        film = await cur.fetchone()
        return film