from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BigInteger

import database

# 데이터베이스 테이블 모델링 (ORM)

# user: 사용자 기본 정보에 관한 테이블
class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(40), unique=True, index=True)
    hashed_password = Column(String(100))
    reg_date = Column(Date, nullable=True)

    profiles = relationship("Profile", back_populates="owner")

# profile: 사용자 프로필 정보 테이블
# 현재 사용자와 프로필은 1대 다 관계를 이루고 있다.
class Profile(database.Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    alias = Column(String(20), index=True)
    department = Column(String(20))
    prefer_dark = Column(Boolean, default=False)
    subscribing = Column(Boolean, default=True)
    tel = Column(String(20))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="profiles")