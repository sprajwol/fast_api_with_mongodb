
import enum
import json

# def userEntity(item) -> dict:
#     return {
#         "id": str(item['_id']),
#         "name": item["name"],
#         "email": item["email"],
#         "password": item['password'],
#         "role": item['role']
#     }


# def usersEntity(entity) -> list:
#     return [userEntity(item) for item in entity]


def serializeDict(a) -> json:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]


def waitingApprovalDict(item) -> dict:
    return {
        "id": str(item['_id']),
        "name": item["name"],
        "email": item["email"],
        "role": item['role'],
        "is_approved": item['is_approved']
    }

def waitingApprovalList(entity) -> list:
    return [waitingApprovalDict(a) for a in entity]