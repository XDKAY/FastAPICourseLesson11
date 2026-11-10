import string
from uuid import uuid4
from typing import Annotated
from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    ConfigDict,
    field_validator,
)


__all__ = (
    "UserRequestScheme",
    "UserResponseScheme",
)


class UserBaseModel(BaseModel):
    username: Annotated[
        str,
        Field(
            examples=["Alex"],
            min_length=3
        )
    ]
    password: Annotated[
        SecretStr,
        Field(
            examples=["qwerty123!ABC"],
            min_length=8,
            max_length=20
        )
    ]

    @field_validator("username")
    @classmethod
    def _validate_usename(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("Имя пользователя должно состоять только из букв")

        return value

    @field_validator("password")
    @classmethod
    def _validate_password(cls, password: SecretStr) -> SecretStr:
        value = password.get_secret_value()

        if not any(char in value for char in string.ascii_lowercase):
            raise ValueError("Пароль должен содержать хотя бы одну букву в нижнем регистре")

        if not any(char in value for char in string.ascii_uppercase):
            raise ValueError("Пароль должен содержать хотя бы одну букву в верхнем регистре")

        if not any(char in value for char in string.digits):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")

        if not any(char in value for char in string.punctuation):
            raise ValueError("Пароль должен содержать хотя бы один знак пунктуации")

        return password


class UserRequestScheme(UserBaseModel):
    ...


class UserResponseScheme(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

    id: str
    username: str
    password: Annotated[SecretStr, Field(exclude=True)]
