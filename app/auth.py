from typing import Optional

from fastapi import HTTPException, status

from .schemes import (
    UserResponseScheme
)

from .database import UserDatabase


__all__ = (
    "auth_user",
)


def auth_user(username: str, password: str) -> Optional[UserResponseScheme]:
    database = UserDatabase()

    user_model = database.get_by_username(username)

    if not user_model:
        return None

    if user_model.password.get_secret_value() == password:
        return user_model

    elif user_model.password.get_secret_value() != password:
        return None
