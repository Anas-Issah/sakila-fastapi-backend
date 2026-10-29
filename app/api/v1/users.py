from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm

from database.connection import get_db
from schemas.user import NewUser
import services.user_services as user_services

router = APIRouter(
    prefix="/users",
    tags=["User"]
)




@router.post("/create")
async def create_user(new_user:NewUser,conn=Depends(get_db)):

    return user_services.create_user(new_user.username,new_user.password,conn)

@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends(),
                conn = Depends(get_db)):

    return user_services.get_user(form.username,form.password,conn)

