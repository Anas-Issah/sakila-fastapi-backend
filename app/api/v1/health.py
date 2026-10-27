from fastapi import APIRouter

import database.health_connect as connect

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/databasae")
async def database_rediness():

    conn =  connect.get_db()

    with conn.cursor() as cur:
        cur.execute("SELECT 1")

        respone = cur.fetchone()

        if not respone:
            raise ValueError

    return {
        "statu":"healthy",
        "details":"Database connected"
    }

