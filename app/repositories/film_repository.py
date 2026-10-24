
def get_film(film_id:int,conn):
     with conn.cursor() as cur:
            cur.execute(
                "SELECT film_id,title,release_year,length,rating " \
                "FROM film " \
                "WHERE film_id = %s",(film_id,)
    
            )
    
            return cur.fetchone()


def get_films(offset:int|None,limit:int|None,conn):

    params = []

    query = "SELECT film_id, title, release_year,length,rating " \
                    "FROM film ORDER BY film_id " 

    if offset:
        params.append(offset)
        query = query + " OFFSET %s "

    if limit:
        params.append(limit)
        query = query + "LIMIT %s"
    
    with conn.cursor() as cur:
        cur.execute(query,params)

        return cur.fetchall()


def search_by_title(film_title:str,conn):

    with conn.cursor() as cur:

        query = "SELECT film_id, title, release_year,length,rating " \
                           "FROM film " \
                           "WHERE title = %s"

        cur.execute(query,(film_title,))

        return cur.fetchone()
