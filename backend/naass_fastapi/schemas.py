from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ProfileBase(BaseModel):
    alias: str


class ProfileCreate(ProfileBase):
    name: Optional[str] = None
    department: Optional[str] = None
    tel: Optional[str] = None


class Profile(ProfileBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    reg_date: Optional[date] = None
    profiles: List[Profile] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None