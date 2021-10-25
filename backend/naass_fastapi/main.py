from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models
from .schemas import Profile, ProfileCreate, User, UserCreate
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/profiles", response_model=Profile)
async def create_profile_for_user(user_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile, user_id=user_id)


@app.get("/profiles", response_model=List[Profile])
async def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_profiles(db, skip=skip, limit=limit)


@app.put('/profiles/{profile_id}')
async def edit_profile(profile_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(400, 'profile not found')
    return crud.update_profile(db, profile_id, profile)
