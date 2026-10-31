import os
import uuid
import time
import jwt
from pwdlib import PasswordHash
from datetime import datetime,timezone,timedelta
from pathlib import Path
from dotenv import load_dotenv

from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from exceptions.users import UsernameTaken,UserNotFound,WrongUserPassword
import repositories.users as repo_users


oauth2_scheme = OAuth2PasswordBearer("/api/v1/users/login")

load_dotenv(Path.cwd().parent/"app"/".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

revoked_refresh_tokens = set()
user_requests = {}

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


def create_token(user_id:str,username:str,token_type:str):

    expire_delta = timedelta(minutes=15) if token_type == "access" else timedelta(days=10)

    payload = {
        "user_id":str(user_id),
        "username":username,
        "token_type":token_type,
        "jti":str(uuid.uuid4()),
        "exp":datetime.now(timezone.utc) + expire_delta
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    

def login(username:str,password:str,conn):

    user = repo_users.get_user(username,password,conn)

    if not user:
        raise UserNotFound

    user_id,hashed_password = user
    password_hash = PasswordHash.recommended()

    if not password_hash.verify(
        password,
        hashed_password
    ):
        raise WrongUserPassword

    access_token = create_token(user_id,username,"access")
    refresh_token = create_token(user_id,username,"refresh")

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }


def logout(token:str ):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    
    revoked_refresh_tokens.add(payload["jti"])

    return {"message":"Successfully logged out"}


def refresh_token(token):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="expired token"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )


    user_id = payload["user_id"]
    username = payload["username"]
    token_type = payload["token_type"]

    if not payload["token_type"] == "refresh":
        raise HTTPException(
            status_code=401,
            detail="refresh token needed"
        )

    if payload["jti"] in revoked_refresh_tokens:
        raise HTTPException(
            status_code=401,
            detail="Revoked token reuse detected"
        )

    revoked_refresh_tokens.add(payload["jti"])

    access_token = create_token(user_id,username,"access")
    refreh_token = create_token(user_id,username,"refresh")  

    print("Token refreshed")  

    return{
        "access_token":access_token,
        "refresh_token":refreh_token,
        "token_type":"Bearer"
    }

def get_current_user(token:str=Depends(oauth2_scheme)):
   
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload["jti"] in revoked_refresh_tokens:
            raise HTTPException(
                status_code=401,
                detail="Revoked token"
            )

    except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="expired token"
            )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )

    return payload

def  user_rate_limit(rate:int,window:int):

    def rate_limit_checker(payload = Depends(get_current_user)):

        current_time = time.time()

        user_id =  payload["user_id"]

        if not user_id in user_requests:
            user_requests[user_id] = []

        user_requests[user_id] = [timestamp for timestamp in user_requests[user_id]
                                  if current_time - timestamp < window]

        if len(user_requests[user_id]) >= rate:
            raise HTTPException(
                status_code=429,
                detail="Too many request"
            )

        user_requests[user_id].append(current_time)

    return rate_limit_checker