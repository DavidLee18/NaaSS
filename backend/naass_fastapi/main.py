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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

# db를 로드하는 function
async def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# password를 입력하면 db에 저장된 해시 상태의 비밀번호와 일치하는지 확인한다
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#비밀번호를 해시한다
def get_password_hash(password):
    return pwd_context.hash(password)

#JWT 토큰을 생성한다
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#쿠키에 있는 JWT 토큰에 저장된 email로 db에서 사용자를 읽어와 반환한다
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

#user가 실제로 db에 있는 사용자인지 검증한 후 반환한다.
def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#JWT 토큰을 이용해 비밀번호 재설정 메일 본문을 반환한다
def get_email_html(access_token: str):
    return f"""<p>
    이 메일은 본 메일주소로 등록된 NaaSS 계정의 비밀번호 재설정을 위해 발송되었습니다 <br>
    비밀번호를 재설정 하시려면 
    <a href="https://naass.nginxplus.co.kr/forgot-password?token={access_token}">이 링크</a>를
    통해서 재설정하세요 <br>
    NaaSS - NGINX as a subscription service
    </p>"""


#API

#로그인 되어 있을 경우 자기 자신의 사용자 정보를 가져온다
@app.get('/api/users/me')
async def read_items(current_user: schemas.UserCreate = Depends(get_current_user)):
    return current_user

#email과 password로 로그인해서 JWT 토큰을 쿠키로 반환한다
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

#요청에 있는 쿠키를 삭제함으로써 로그아웃한다
@app.delete('/api/token')
async def logout(current_user: schemas.UserCreate = Depends(get_current_user)):
    res = Response()
    res.delete_cookie('access')
    return res

#email을 받아서 비밀번호 재설정 메일을 보낸다
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

#비밀번호 재설정 메일에 포함된 JWT 토큰과 새로운 비밀번호를 받아 해당 사용자의 비밀번호를 변경한다
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

#회원가입하여 사용자를 추가한다
@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user_form.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DUPLICATE_EMAIL")
    return crud.create_user(db=db, user=schemas.UserCreate(
        email=user_form.username,
        hashed_password=get_password_hash(user_form.password)
        ))

#전체 사용자를 가져온다
@app.get("/api/users")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    return crud.get_users(db, skip=skip, limit=limit)

#user id로 특정 사용자를 가져온다
@app.get("/api/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#user id로 특정 사용자를 삭제한다
@app.delete('/api/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    succeeded = crud.delete_user(db, user_id)
    if not succeeded:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'user to delete is not found'
        )

#특정 사용자의 프로필을 생성한다
@app.post("/api/users/{user_id}/profiles", status_code=status.HTTP_201_CREATED)
async def create_profile_for_user(user_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    return crud.create_profile(db=db, profile=profile, user_id=user_id)

#전체 프로필들을 가져온다 (*특정 사용자의 프로필만 가져오는 기능 필요)
@app.get("/api/profiles")
async def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    return crud.get_profiles(db, skip=skip, limit=limit)

#profile id로 특정 프로필을 가져온다
@app.put('/api/profiles/{profile_id}')
async def edit_profile(profile_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    db_profile = crud.get_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'profile not found')
    return crud.update_profile(db, profile_id, profile)

#profile id로 특정 프로필을 삭제한다
@app.delete('/api/profiles/{profile_id}')
async def delete_profile(profile_id: int, db: Session = Depends(get_db), current_user: schemas.UserCreate = Depends(get_current_user)):
    succeeded = crud.delete_profile(db, profile_id)
    if not succeeded:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'profile to delete is not found'
        )