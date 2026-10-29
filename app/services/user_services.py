import os
import uuid
import jwt
from pwdlib import PasswordHash
from datetime import datetime,timezone,timedelta
from pathlib import Path
from dotenv import load_dotenv

from exceptions.users import UsernameTaken
import repositories.users as repo_users


load_dotenv(Path.cwd().parent/"app"/".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def hashed_word(password:str):

    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def create_user(username:str,password:str,conn):

    # check if username already exist
    name = repo_users.check_username(username,conn)

    if name:
        raise UsernameTaken

    user_id = uuid.uuid4()

    hashed_password = hashed_word(password)

    

   
    new_user = repo_users.create_user(user_id,username,hashed_password,conn)

    return {
        "status_code":200,
        "details":f"User {new_user[0]} created successfully"
    }


def create_token(user_id:str,username:str,token_type,expire_delta):

    payload = {
        "user_id":str(user_id),
        "username":username,
        "token_type":token_type,
        "exp":datetime.now(timezone.utc) + expire_delta
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    

def get_user(username:str,password:str,conn):

    user = repo_users.get_user(username,password,conn)

    if not user:
        raise ValueError

    user_id,hashed_password = user
    password_hash = PasswordHash.recommended()

    if not password_hash.verify(
        password,
        hashed_password
    ):
        raise ValueError

    access_token = create_token(user_id,username,"access",timedelta(minutes=30))

    return {
        "access token":access_token,
        "token_typen":"bearer"
    }

def get_current_user(token:str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise

    except jwt.InvalidTokenError:
        raise

    return payload