from typing import Sequence
from uuid import UUID

from model.tasks import Tasks
from schemas.user import TaskInput, TaskType
from sqlalchemy import select
from utils.database.async_database import sessionmanager


class CreateMutation:
	async def add_task(self, tasks_data: TaskInput) -> Tasks:
		async with sessionmanager.async_session() as session:
			task = Tasks(**tasks_data.__dict__)
			session.add(task)
			await session.commit()
			await session.refresh(tasks_data)
			return task


class Queries:
	async def get_tasks(self, user_id: UUID) -> Sequence[TaskType]:
		async with sessionmanager.async_session() as session:
			stmt = select(Tasks).where(Tasks.user_id == user_id)
			result = await session.execute(stmt)
			return result.scalars().all()

	async def get_task(self, task_id: UUID, user_id: UUID) -> TaskType | None:
		async with sessionmanager.async_session() as session:
			stmt = (
				select(Tasks).where(Tasks.id == task_id).where(Tasks.user_id == user_id)
			)
			result = await session.execute(stmt)
			return result.scalar_one_or_none()
