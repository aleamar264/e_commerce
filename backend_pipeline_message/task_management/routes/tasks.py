from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_login import LoginManager
from schemas.user import User
from utils.fastapi.auth.secret_key import secret_key

SECRET_KEY = secret_key.secret_key
manager = LoginManager(
	token_url="http://localhost:8000/auth/token", secret=SECRET_KEY, use_cookie=True
)
manager.cookie_name = "auth"


@manager.user_loader()
def load_user(identifier: str) -> User:
	username, role, id_ = identifier.split("_*")
	return User(username=username, role=role, id=UUID(id_))


tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_router.get("/")
async def get_tasks(user=Depends(manager)) -> User:
	return user


# TODO: This endpoint with graphql
# TODO: Create Tasks
# Request Body: JSON containing task details (e.g., title, description, due date, assigned user ID).
# Functionality:
# Validate user ID using a call to the User Management service (explained later).
# Persist the task data in the Task Management database.
# Optionally, publish a message to the message broker notifying other services (e.g., Recommendation Engine) about the new task.

# TODO: Get all tasks
# Functionality:
# Retrieve all tasks from the database.
# Consider filtering or pagination for large numbers of tasks.

# TODO: Get task by ID
# Path Parameter: task_id (unique identifier for the task).
# Functionality:
# Retrieve the specific task with the given ID from the database.
# Return an error if the task ID is not found

# TODO: Update Task (PUT /tasks/{task_id}):
# Path Parameter: task_id
# Request Body: JSON containing updated task details.
# Functionality:
# Validate user ID in the updated data using a call to User Management.
# Update the task data in the database based on the provided ID and details.
# Optionally, publish a message to the message broker notifying other services about the task update.

# TODO: Mark Task as Complete (PATCH /tasks/{task_id}/complete):
# Path Parameter: task_id
# Functionality:
# Update the task's completion status to "completed" in the database.
# Optionally, publish a message to the message broker notifying other services about the task completion.

# TODO: Delete task by ID
# Path Parameter: task_id
# Functionality:
# Delete the task with the given ID from the database.
# Return an error if the task ID is not found.
