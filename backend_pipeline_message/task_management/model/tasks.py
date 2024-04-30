import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.database.async_database import Base
from utils.database.general import MixInNameTable


class User(Base, MixInNameTable):
	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, index=True
	)
	username: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
	is_active: Mapped[bool] = mapped_column(default=False)
	role: Mapped[str] = mapped_column(nullable=False)
	tasks: Mapped[list["Tasks"]] = relationship(back_populates="user")


class Tasks(Base, MixInNameTable):
	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		default=uuid.uuid4,
		index=True,
		unique=True,
		primary_key=True,
	)
	name: Mapped[str] = mapped_column(nullable=False)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("user.id"),
		nullable=True,
		index=True,
	)
	user: Mapped["User"] = relationship(back_populates="tasks")
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		index=True,
		default=datetime.now(UTC),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		index=True,
		onupdate=datetime.now,
		default=datetime.now(UTC),
	)
	description: Mapped[str] = mapped_column(String, nullable=True)
	is_completed: Mapped[bool] = mapped_column(default=False)
