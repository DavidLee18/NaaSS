from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import crud, models, schemas, database


database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Dependency
async def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fake_decode_token(db: Session, token: str):
    return crud.get_user_by_email(db, email=token)

def fake_hash_password(password: str):
    return password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = fake_decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Authentication Credentials',
            headers={ 'WWW-Authenticate': 'Bearer' },
        )
    return user

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



#test
@app.get('/users/me')
async def read_items(current_user: schemas.UserCreate = Depends(get_current_user)):
    return current_user

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    return { 'access_token': user.email, 'token_type': 'bearer' }

#real apis
@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/profiles", response_model=schemas.Profile)
async def create_profile_for_user(user_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile, user_id=user_id)


@app.get("/profiles", response_model=List[schemas.Profile])
async def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_profiles(db, skip=skip, limit=limit)


@app.put('/profiles/{profile_id}')
async def edit_profile(profile_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(400, 'profile not found')
    return crud.update_profile(db, profile_id, profile)
