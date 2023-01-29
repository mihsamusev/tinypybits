
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel

import auth
from model import User
from repository.in_memory_db import InMemoryUsersDB, get_users_db

app = FastAPI()

# keeper of the jwt token of the currently logged in user
# once token is set through POST <tokenURL>
# the scheme will look for 
# Bearer + token in the Authorization header of the request
# and compare to the token it keeps
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def login_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )



async def get_current_user(
    db: InMemoryUsersDB = Depends(get_users_db),
    encoded_token: str = Depends(oauth2_scheme)
):
    print(f"found token: {encoded_token}")
    try:
        payload = auth.decode_token(encoded_token)
    except JWTError:
        raise login_exception("Login session has expired")

    username = payload.get_subject()
    if not username:
        raise login_exception("Invalid authentification credentials")

    user = db.get_user(username=username)
    if not user:
        raise login_exception("Invalid authentification credentials")

    return user


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@app.post("/token")
async def login_for_access_token(
    db: InMemoryUsersDB = Depends(get_users_db),
    form: OAuth2PasswordRequestForm = Depends()
    ):
    user = auth.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = auth.create_access_token(subject=user.username)
    response = TokenResponse(access_token=token, token_type="bearer")
    return response


@app.get("/good_stuff")
async def good_stuff(user: User = Depends(get_current_user)):
    return {"response": "welcome back " + user.username}
