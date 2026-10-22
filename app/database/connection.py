from psycopg_pool import ConnectionPool


pool = ConnectionPool(
    """dbname=dvd_rental
    user=postgres
    host=localhost
    password=BEBOANO12""",
    min_size=5,max_size=10
)
def get_db():

    with pool.connection() as conn:
        yield conn
