from typing import Optional

from .models import UserModel
from .schemes import (
    UserResponseScheme,
    UserRequestScheme,
)


__all__ = (
    "UserDatabase",
)


class UserDatabase:

    __MODEL = UserModel
    __DATA: list[__MODEL] = []

    def add(self, user: UserRequestScheme) -> UserResponseScheme:
        user_model = self.__MODEL.model_validate(user)

        self.__DATA.append(user_model)

        return UserResponseScheme.model_validate(user_model)

    def get_by_username(self, username: str) -> Optional[UserResponseScheme]:
        for user in self.__DATA:
            print(user)
            if user.username == username:
                return UserResponseScheme.model_validate(user)

        return None

    def get_by_id(self, id: str) -> Optional[UserResponseScheme]:
        for user in self.__DATA:
            if user.id == id:
                return UserResponseScheme.model_validate(user)

        return None
