import uuid
from datetime import datetime

from schemas.user import Roles
from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from utils.database.async_database import Base
from utils.database.general import MixInNameTable


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
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), nullable=False, index=True
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), nullable=False, index=True, onupdate=datetime.now
	)
	hashed_password: Mapped[str] = mapped_column(nullable=False)
	city: Mapped[str] = mapped_column(nullable=True, default=None)
	street: Mapped[str] = mapped_column(nullable=True, default=None)
	country: Mapped[str] = mapped_column(nullable=True, default=None)
	state: Mapped[str] = mapped_column(nullable=True, default=None)
	zip_code: Mapped[int] = mapped_column(nullable=True, default=None)
	phone: Mapped[int] = mapped_column(nullable=True, default=None)
	activation_key: Mapped[str] = mapped_column(nullable=True, default=None)
