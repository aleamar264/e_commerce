from datetime import UTC, datetime
from enum import Enum

from pydantic import UUID4, BaseModel, EmailStr, Field, SecretStr


class Roles(str, Enum):
	admin = "admin"
	user = "user"


def datetime_now():
	return datetime.now(UTC)


class UserBase(BaseModel):
	email: EmailStr
	username: str = Field(max_length=25)
	name: str
	last_name: str | None = None
	is_active: bool = False
	role: Roles = Field(default=Roles.user)
	created_at: datetime = Field(default_factory=datetime_now)
	updated_at: datetime = Field(default_factory=datetime_now)
	hashed_password: SecretStr


class User(UserBase):
	id: UUID4


class UpdatePassword(BaseModel):
	id: UUID4
	old_password: SecretStr
	new_password: SecretStr = Field(min_length=8)
