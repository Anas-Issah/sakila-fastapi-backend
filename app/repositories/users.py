from psycopg.rows import dict_row

def check_username(username:str,conn):

    query ="SELECT * FROM users WHERE username = %s"
    with conn.cursor() as cur:
        cur.execute(query,(username,))

        return cur.fetchone()


def create_user(user_id,username:str,password_hash:str,conn):

    query = "INSERT INTO users VALUES(%s,%s,%s)"
    query += "RETURNING username"

    with conn.cursor() as cur:

        cur.execute(query,(user_id,username,password_hash))

        return cur.fetchone()

async def get_user(username:str,password:str,conn):

    query = "SELECT user_id,password_hash "
    query += "FROM users "
    query += "WHERE username = %s"

    async with conn.cursor() as cur:
        await cur.execute(query,(username,))

        return await cur.fetchone() 