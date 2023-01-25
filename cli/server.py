import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ASSESS_JWT_EXPIRE_MINUTES = os.getenv("ACCESS_JWT_EXPIRE_MINUTES")

class User(BaseModel):
    username: str


class UserDB(User):
    hashed_password: str

class Token(BaseModel):
    assess_token: str
    token_type: str

class Tokendata(BaseModel):
    username: str


fake_users_db = {
    "alice": {"username": "alice", "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"},
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserDB(**user_dict)


def hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token):
    return get_user(fake_users_db, token)


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Given the token, who is the user?
    """
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentification credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Verify username and password -> give token
    predefined OAuth2 form_data (username, password, scope[])
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserDB(**user_dict)
    hashed_password = hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response = {"access_token": user.username, "token_type": "bearer"}
    return response


@app.get("/good_stuff")
async def good_stuff(user: User = Depends(get_current_user)):
    return user
