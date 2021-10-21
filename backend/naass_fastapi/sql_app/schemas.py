from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class ProfileBase(BaseModel):
    alias: str


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    owner_id: int
    name: Optional[str] = None
    department: Optional[str] = None
    tel: Optional[str] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    reg_date: Optional[date] = None
    profiles: List[Profile] = []

    class Config:
        orm_mode = True
