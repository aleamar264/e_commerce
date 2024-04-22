import uuid

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .utils.database.async_database import Base
from .utils.database.general import MixInNameTable


class User(Base, MixInNameTable):
	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		primary_key=True,
		default=uuid.uuid4,
		index=True,
		unique=True,
	)
	email: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
	username: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
	name: Mapped[str] = mapped_column(nullable=False)
	last_name: Mapped[str] = mapped_column(nullable=True)
	is_active: Mapped[bool] = mapped_column(default=False)
	role: Mapped[Roles] = mapped_column(
		Enum(Roles), nullable=False, default=Roles.user, index=True
	)
	created_at: Mapped[DateTime] = mapped_column(nullable=False, index=True)
	updated_at: Mapped[DateTime] = mapped_column(nullable=False, index=True)
	hashed_password: Mapped[str] = mapped_column(nullable=False)
