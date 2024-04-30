from typing import Sequence

import strawberry
from schemas.user import TaskType

from .controller import CreateMutation, Queries


@strawberry.type
class Mutation:
	add_tasks: TaskType = strawberry.mutation(resolver=CreateMutation.add_task)


@strawberry.type
class Query:
	get_tasks: Sequence[TaskType] = strawberry.field(resolver=Queries.get_tasks)
	get_task: TaskType = strawberry.field(resolver=Queries.get_task)
