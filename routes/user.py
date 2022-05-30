import json
from pprint import pprint
from bson import ObjectId, json_util 
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from models.user import User, Token
from utils import utils, oauth2

from config.db import conn
from schemas.user import serializeDict, serializeList

user = APIRouter()

from pymongo.errors import WriteError

@user.get('/')
async def find_all_users():
    # print(f"conn.pymongo.user.find() ::: {conn.pymongo.user.find()}")
    # print(
    #     f"usersEntity(conn.pymongo.user.find()) ::: {usersEntity(conn.pymongo.user.find())}")
    return serializeList(conn.pymongo.user.find())

@user.get('/{id}')
async def find_one_user(id, current_user: int = Depends(oauth2.get_current_user)):
    return serializeDict(conn.pymongo.user.find_one({"_id": ObjectId(id)}))



@user.post('/', status_code=201)
async def create_user(user: User):
    # print(f"user:{user}")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # print(f"user:{user}")
    
    try:
        user = conn.pymongo.user.insert_one(dict(user))
        # print(f"user:{user['_id']}")
    except WriteError as e:
        raise HTTPException(status_code=400,detail=json.loads(json_util.dumps(e.details)))
    return serializeList(conn.pymongo.user.find({}))


@user.put('/{id}')
async def update_user(id, user: User, current_user: int = Depends(oauth2.get_current_user)):
    conn.pymongo.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return serializeDict(conn.pymongo.user.find_one({"_id": ObjectId(id)}))


@user.delete('/{id}', dependencies=[Depends(oauth2.RoleChecker(['admin']))])
async def delete_user(id, current_user: int = Depends(oauth2.get_current_user)):
    
    return serializeDict(conn.pymongo.user.find_one_and_delete({"_id": ObjectId(id)}))


@user.post('/login', response_model=Token)
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

    # Create a token
    # return token
    # print("user", user['_id'])
    access_token = oauth2.create_access_token(data={"user_id": user['_id']})

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
