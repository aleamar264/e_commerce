from typing import Sequence, override
from uuid import UUID

from models.user import User
from schemas.user import User as user_schema
from sqlalchemy import select
from utils.database.async_database import depend_db_annotated
from utils.database.crud.general import GeneralCrudAsync
from utils.fastapi.exceptions.exceptions_user import (
	EntityAlreadyExistsError,
	EntityDoesNotExistError,
)


class UserCrudAsync(GeneralCrudAsync[User]):
	def __init__(self, model=User, session=depend_db_annotated) -> None:
		super().__init__(model, session)

	@override
	async def get_users(self) -> Sequence[User]:
		stmt = select(self.model)
		result = await self.session.execute(stmt)
		return result.scalars().all()

	@override
	async def get_user_by_email(self, email: str) -> User:
		stmt = select(self.model).where(self.model.email == email)
		result = await self.session.execute(stmt)
		if not (user := result.first()):
			raise EntityDoesNotExistError(message="User don't exist")
		return user

	@override
	async def get_user_by_id(self, user_id: UUID) -> User:
		stmt = select(self.model).where(self.model.id == user_id)
		result = await self.session.execute(stmt)
		if not (user := result.first()):
			raise EntityDoesNotExistError(message="User don't exist")
		return user

	@override
	async def get_user_by_username(self, username: str) -> User:
		stmt = select(self.model).where(self.model.username == username)
		result = await self.session.execute(stmt)
		if (user := result.scalar_one_or_none()) is None:
			raise EntityDoesNotExistError(message="User don't exist")
		return user

	@override
	async def delete_user(self, user_id: UUID) -> None:
		user = await self.get_user_by_id(user_id)
		await self.session.delete(user)
		await self.session.commit()

	@override
	async def create_user(self, user: user_schema) -> User:
		user_ = await self.get_user_by_email(user.email)
		if user_:
			raise EntityAlreadyExistsError(
				message=f"User with email {user.email} alerady is registered"
			)
		user_ = self.model(**user.model_dump())
		stmt = self.session.add(user_)
		await self.session.commit()
		await stmt.refresh(user_)
		return user_

	@override
	async def update_user(self, user: user_schema) -> User | None:
		user_ = await self.get_user_by_id(user.id)
		if not user_:
			raise EntityDoesNotExistError(message="User don't exist")
		for attr, value in user.model_dump().items():
			setattr(user_, attr, value)
		await self.session.commit()
		await self.session.refresh(user_)
		return user_


user_crud = UserCrudAsync()
