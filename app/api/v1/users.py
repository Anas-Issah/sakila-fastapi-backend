from fastapi import APIRouter,Depends

from database.connection import get_db
from schemas.user import NewUser
import services.user_services as user_services

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("")
async def create_user(new_user:NewUser,conn=Depends(get_db)):

    return user_services.create_user(new_user.username,new_user.password,conn)