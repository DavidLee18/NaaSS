from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

import database


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(100))
    reg_date = Column(Date, nullable=True)

    profiles = relationship("Profile", back_populates="owner")


class Profile(database.Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    alias = Column(String(20), index=True)
    department = Column(String(20))
    prefer_dark = Column(Boolean, default=False)
    tel = Column(String(20))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="profiles")
