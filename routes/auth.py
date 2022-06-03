
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.user import User, Token
from config.db import conn
from schemas.user import serializeDict, serializeList
from utils import utils, oauth2

auth = APIRouter(
    tags=["Auth"]
)

@auth.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    # print("user_credentials.username",user_credentials.username)
    user = serializeDict(conn.pymongo.user.find_one({"email": user_credentials.username}))
    # print(user)
    # print(user['password'])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password,  user['password']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not user["is_approved"] == True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Account has not been approved. Please contact your admin.")

    # Create a token
    # return token
    # print("user", user['_id'])
    access_token = oauth2.create_access_token(data={"user_id": user['_id']})

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
