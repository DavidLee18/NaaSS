from datetime import date
from typing import List, Optional

from pydantic import BaseModel

# profile의 최상위 클래스
class ProfileBase(BaseModel):
    alias: str

# profile을 코드에서 생성할 때 사용하는 클래스
class ProfileCreate(ProfileBase):
    name: Optional[str] = None
    department: Optional[str] = None
    prefer_dark: Optional[bool] = None
    subscribing: Optional[bool] = None
    tel: Optional[str] = None

# db profile과 대응하는 클래스
class Profile(ProfileBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# user의 최상위 클래스
class UserBase(BaseModel):
    email: str

# user를 코드에서 생성할 때 사용하는 클래스
class UserCreate(UserBase):
    hashed_password: str

# db user와 대응하는 클래스
class User(UserBase):
    id: int
    reg_date: Optional[date] = None
    profiles: List[Profile] = []

    class Config:
        orm_mode = True

# 비밀번호 재설정 요청에 이용하는 request body
class ForgotPasswordPacket(BaseModel):
    email: str

# 비밀번호 재설정에 이용하는 request body
class ResetPasswordPacket(BaseModel):
    token: str
    password: str