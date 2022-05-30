from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from bson import ObjectId, json_util 

from models.user import TokenData, User
from config.db import conn
from schemas.user import serializeDict, serializeList

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "11f9b332f4214b605e323dbd6cf3d5250085790381d02da21b2ef2bd9a314a54"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW_Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = conn.pymongo.user.find_one({"_id":ObjectId(token.id)})
    user = serializeDict(user)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        # user = serializeDict(user)
        # print(user)
        if user['role'] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")