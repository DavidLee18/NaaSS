from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

import models, schemas

#user CRUD

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.hashed_password, reg_date=date.today())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False
    else:
        db.delete(user)
        db.commit()
        return True

#profile CRUD

def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()



def create_profile(db: Session, profile: schemas.ProfileCreate, user_id: int):
    db_profile = models.Profile(**profile.dict(), owner_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile: schemas.ProfileCreate):
    db.query(models.Profile).filter(models.Profile.id == profile_id).update({
        models.Profile.alias: profile.alias,
        models.Profile.name: profile.name,
        models.Profile.department: profile.department,
        models.Profile.prefer_dark: profile.prefer_dark,
        models.Profile.tel: profile.tel
    })
    db.commit()

def delete_profile(db: Session, profile_id: int) -> bool:
    profile = get_profile(db, profile_id)
    if profile is None:
        return False
    else:
        db.delete(profile)
        db.commit()
        return True