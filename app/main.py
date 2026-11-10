from typing import Annotated, Optional

from fastapi import (
    FastAPI,
    Response,
    Cookie,
    Depends,
    HTTPException,
    status,
)

from .schemes import (
    UserRequestScheme,
    UserResponseScheme
)
from .database import UserDatabase
from .auth import auth_user


app = FastAPI(
    title="FastAPI Course Lesson 11"
)


DatabaseDep = Annotated[UserDatabase, Depends(UserDatabase)]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Hello World!"
    }


@app.post(
    "/register",
    response_model=UserResponseScheme,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"]
)
def register_endpoint(
    user: UserRequestScheme,
    database: DatabaseDep
):
    exisisting_user = database.get_by_username(user.username)
    if exisisting_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем уже существует"
        )
    user_response = database.add(user)
    return user_response


@app.post("/login", tags=["Auth"])
def login_endpoint(
    user: UserRequestScheme,
    response: Response,
) -> dict[str, str]:

    exisisting_user = auth_user(user.username, user.password.get_secret_value())

    if not exisisting_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильное имя пользователя или пароль"
        )

    response.set_cookie(
        key="session_token",
        value=exisisting_user.id,
        max_age=3600,
        httponly=True
    )

    return {
        "message": "Добро пожаловать!"
    }


@app.post("/logout", tags=["Auth"])
def logout_handler(response: Response) -> dict[str, str]:
    response.delete_cookie(
        key="session_token"
    )

    return {
        "message": "Как-нибудь заглядывай)"
    }


@app.get("/user", tags=["User"])
def me_endpoint(
    database: DatabaseDep,
    session_token: Optional[str] = Cookie(default=None)
) -> UserResponseScheme:

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован"
        )

    user = database.get_by_id(session_token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователя нет в системе"
        )

    return user
