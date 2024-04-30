from datetime import datetime

import strawberry
from pydantic import UUID4, BaseModel


class Task(BaseModel):
	id: UUID4
	name: str
	user_id: UUID4
	created_at: datetime
	description: str
	is_completed: bool


class User(BaseModel):
	id: UUID4
	role: str
	username: str
	tasks: list[Task]


@strawberry.type
class TaskType:
	id: UUID4
	name: str
	user_id: UUID4
	created_at: datetime
	description: str
	is_completed: bool


@strawberry.experimental.pydantic.input(model=User)
class UserType:
	id: strawberry.auto
	role: strawberry.auto
	username: strawberry.auto
	tasks: TaskType


@strawberry.input
class TaskInput:
	name: str
	user_id: UUID4
	description: str
