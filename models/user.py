from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException


ALL_ROLES = ["admin", "staff", "customer"]

class ROLES_M(Enum):
    ADMIN = 'admin'
    STAFF = 'staff'
    CUSTOMER = 'customer'

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: ROLES_M = ROLES_M.CUSTOMER

    class Config:  
        use_enum_values = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

