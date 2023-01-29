import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from model import User

load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_TOKEN_EXPIRE_MINUTES"))
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenPayload(BaseModel):
    sub: str
    exp: datetime

    def get_subject(self):
        return self.sub


def verify_password(raw_password: str, hashed_password: str):
    return password_context.verify(raw_password, hashed_password)


def hash_password(raw_password: str):
    return password_context.hash(raw_password)


def authenticate_user(db, username: str, raw_password: str):
    db_user = db.get_user(username)
    if not db_user:
        return False
    if not verify_password(raw_password, db_user.hashed_password):
        return False
    return db_user


def create_access_token(subject: str) -> str:
    expiration_datetime = datetime.utcnow() + timedelta(
        minutes=JWT_TOKEN_EXPIRE_MINUTES
    )
    payload = TokenPayload(sub=subject, exp=expiration_datetime)
    return jwt.encode(payload.dict(), JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> TokenPayload:
    token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return TokenPayload(**token_parts)
