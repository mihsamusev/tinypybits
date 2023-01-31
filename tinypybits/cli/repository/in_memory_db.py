from typing import Optional

from model import User


class UserInDB(User):
    hashed_password: str


def get_users_db():
    session = InMemoryUsersDB()
    yield session


class InMemoryUsersDB:
    def __init__(self):
        hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        self._users_db = [UserInDB(username="alice", hashed_password=hashed_password)]

    def get_user(self, username: str) -> Optional[UserInDB]:
        return next(
            (user for user in self._users_db if user.username == username), None
        )
