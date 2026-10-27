import uuid
from pwdlib import PasswordHash

from exceptions.users import UsernameTaken

import repositories.users as repo_users


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