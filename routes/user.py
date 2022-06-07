import json
from pprint import pprint
from bson import ObjectId, json_util 
from fastapi import APIRouter, HTTPException, Depends
from pymongo.errors import WriteError

from models.user import User
from utils import utils, oauth2

from config.db import conn
from schemas.user import serializeDict, serializeList, waitingApprovalList, waitingApprovalDict

user = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user.get('/')
async def find_all_users():
    # print(f"conn.pymongo.user.find() ::: {conn.pymongo.user.find()}")
    # print(s
    #     f"usersEntity(conn.pymongo.user.find()) ::: {usersEntity(conn.pymongo.user.find())}")
    return serializeList(conn.pymongo.user.find({"is_approved":True}))



@user.get('/find')
async def findfind_all_users(token: str = Depends(oauth2.token_auth_scheme)):
    print(f"token ::: {token}")
    # print(s
    #     f"usersEntity(conn.pymongo.user.find()) ::: {usersEntity(conn.pymongo.user.find())}")
    return serializeList(conn.pymongo.user.find({"is_approved":True}))

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


@user.get('/waiting_approvals', dependencies=[Depends(oauth2.RoleChecker(['admin']))])
async def find_all_users_waiting_approval(current_user: int = Depends(oauth2.get_current_user)):
    print(f"conn.pymongo")
    # print(
    #     f"usersEntity(conn.pymongo.user.find()) ::: {usersEntity(conn.pymongo.user.find())}")
    return waitingApprovalList(conn.pymongo.user.find({"is_approved":False}))

@user.post('/waiting_approvals')
async def approve_users():
    return "this is approved"

@user.get('/{id}')
async def find_one_user(id, current_user: int = Depends(oauth2.get_current_user)):
    return serializeDict(conn.pymongo.user.find_one({"_id": ObjectId(id), "is_approved":True}))

@user.put('/{id}')
async def update_user(id, user: User, current_user: int = Depends(oauth2.get_current_user)):
    conn.pymongo.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return serializeDict(conn.pymongo.user.find_one({"_id": ObjectId(id)}))


@user.delete('/{id}', dependencies=[Depends(oauth2.RoleChecker(['admin']))])
async def delete_user(id, current_user: int = Depends(oauth2.get_current_user)):
    
    return serializeDict(conn.pymongo.user.find_one_and_delete({"_id": ObjectId(id)}))

