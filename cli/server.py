import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from model import User
from repository.in_memory_db import InMemoryUsersDB, get_users_db

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ASSESS_JWT_EXPIRE_MINUTES = os.getenv("JWT_TOKEN_EXPIRE_MINUTES")


class Token(BaseModel):
    assess_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str


def hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(db: InMemoryUsersDB, token):
    db_user = db.get_user(username=token)
    return User(db_user) 

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(
    db: InMemoryUsersDB = Depends(get_users_db), token: str = Depends(oauth2_scheme)
):
    """
    Given the token, who is the user?
    """
    user = fake_decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentification credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(db: InMemoryUsersDB = Depends(get_users_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Verify username and password -> give token
    predefined OAuth2 form_data (username, password, scope[])
    """
    user = db.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response = {"access_token": user.username, "token_type": "bearer"}
    return response


@app.get("/good_stuff")
async def good_stuff(user: User = Depends(get_current_user)):
    return user
