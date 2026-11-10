from uuid import uuid4
from datetime import datetime, timezone
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    ConfigDict
)


__all__ = (
    "UserModel",
)


class UserModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4())
        )
    ]
    username: str
    password: SecretStr
    created_at: Annotated[
        datetime,
        Field(
            default_factory=lambda: datetime.now(timezone.utc)
        )
    ]
