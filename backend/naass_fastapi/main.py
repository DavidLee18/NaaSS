from datetime import datetime, timedelta
from typing import Final, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status, Cookie
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import crud, models, schemas, database


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY: Final[str] = "cd3d102089ea57e9ed47373f6067bd6bea4f9f965de8c186ddf7e59e47c07b12"
ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_EXPIRE_TIME: Final[timedelta] = timedelta(minutes=30)

database.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://192.168.200.17:8080"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#app.mount('/', StaticFiles(directory='dist'), 'dist')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

mail_conf = ConnectionConfig(
    MAIL_USERNAME = 'djwodus18',
    MAIL_PASSWORD = '',
    MAIL_FROM = 'djwodus18@naver.com',
    MAIL_PORT = 465,
    MAIL_SERVER = 'smtp.naver.com',
    MAIL_FROM_NAME = 'NaaSS',
    MAIL_TLS = False, # naver mail needs SSL, not TLS
    MAIL_SSL = True,
    USE_CREDENTIALS = True,
)

mail = FastMail(mail_conf)

# Dependency
async def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(access: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Authentication Credentials',
        headers={ 'WWW-Authenticate': 'Bearer' },
    )
    try:
        if access is None:
            raise credentials_exception
        payload = jwt.decode(access, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get('sub')
        if username is None:
            raise credentials_exception
        else:
            user = crud.get_user_by_email(db, email=username)
            if user is None:
                raise credentials_exception
            else:
                return user
    except JWTError:
        raise credentials_exception

def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_email_html(access_token: str):
    return f"""<p>
    이 메일은 본 메일주소로 등록된 NaaSS 계정의 비밀번호 재설정을 위해 발송되었습니다 <br>
    비밀번호를 재설정 하시려면 
    <a href="https://naass.nginxplus.co.kr/forgot-password?token={access_token}">이 링크</a>를
    통해서 재설정하세요 <br>
    NaaSS - NGINX as a subscription service
    </p>"""




@app.get('/api/users/me')
async def read_items(current_user: schemas.UserCreate = Depends(get_current_user)):
    return current_user

@app.post('/api/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={ 'WWW-Authenticate': 'Bearer' }
        )
    access_token = create_access_token({ 'sub': user.email }, ACCESS_TOKEN_EXPIRE_TIME)
    res = Response()
    res.set_cookie("access", access_token, expires=ACCESS_TOKEN_EXPIRE_TIME.seconds, secure=True, httponly=True)
    return res

@app.delete('/api/token')
async def logout(current_user: schemas.UserCreate = Depends(get_current_user)):
    res = Response()
    res.delete_cookie('access')
    return res

@app.post('/api/forgot-password', status_code=status.HTTP_202_ACCEPTED)
async def send_password_reset_email(email: schemas.ForgotPasswordPacket, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email.email)
    if user is not None:
        access_token = create_access_token({ 'sub': email.email }, ACCESS_TOKEN_EXPIRE_TIME)
        message = MessageSchema(
            subject = 'NaaSS: 비밀번호 재설정',
            recipients = [email.email],
            body = get_email_html(access_token),
            subtype = 'html'
        )
        await mail.send_message(message)

@app.post('/api/reset-password')
async def reset_password(token_and_password: schemas.ResetPasswordPacket, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='bad or expired token',
    )
    try:
        if token_and_password.token is None:
            raise credentials_exception
        payload = jwt.decode(token_and_password.token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get('sub')
        if username is None:
            raise credentials_exception
        else:
            user = crud.get_user_by_email(db, email=username)
            if user is None:
                raise credentials_exception
            else:
                crud.update_user(db, schemas.UserCreate(email=user.email, hashed_password=get_password_hash(token_and_password.password)))
                return JSONResponse({ 'detail': 'password successfully reset' })
    except JWTError:
        raise credentials_exception


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_form.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=schemas.UserCreate(
        email=user_form.username,
        hashed_password=get_password_hash(user_form.password)
        ))


@app.get("/api/users")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/api/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete('/api/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    succeeded = crud.delete_user(db, user_id)
    if not succeeded:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'user to delete is not found'
        )


@app.post("/api/users/{user_id}/profiles", status_code=status.HTTP_201_CREATED)
async def create_profile_for_user(user_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    return crud.create_profile(db=db, profile=profile, user_id=user_id)


@app.get("/api/profiles")
async def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    return crud.get_profiles(db, skip=skip, limit=limit)


@app.put('/api/profiles/{profile_id}')
async def edit_profile(profile_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    db_profile = crud.get_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(400, 'profile not found')
    return crud.update_profile(db, profile_id, profile)

@app.delete('/api/profiles/{profile_id}')
async def delete_profile(profile_id: int, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    succeeded = crud.delete_profile(db, profile_id)
    if not succeeded:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'profile to delete is not found'
        )