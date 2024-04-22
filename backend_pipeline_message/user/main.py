from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from routers.user import router as user
from utils.database.async_database import sessionmanager
from utils.fastapi.exceptions import exceptions_user, general


@asynccontextmanager
async def lifespan(_app: FastAPI):
	"""
	    Function that handles startup and shutdown events.
	To understand more, read https://fastapi.tiangolo.com/advanced/events/"""
	yield
	if sessionmanager.engine is not None:
		await sessionmanager.async_close()


app = FastAPI(
	description="API that contain the microservices of the user management/authentication",
	version="0.1.0",
	title="User Management/Authentication API",
	lifespan=lifespan,
)

allow_origins = ["*"]
allow_methods = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=allow_origins,
	allow_credentials=True,
	allow_methods=allow_methods,
	allow_headers=["*"],
)

app.include_router(user)

app.add_exception_handler(
	exc_class_or_status_code=exceptions_user.EntityDoesNotExistError,
	handler=exceptions_user.create_exception_handler(
		status.HTTP_404_NOT_FOUND, "Entity does not exist."
	),
)

app.add_exception_handler(
	exc_class_or_status_code=general.ServiceError,
	handler=exceptions_user.create_exception_handler(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		initial_detail="Internal server error.",
	),
)

app.add_exception_handler(
	exc_class_or_status_code=exceptions_user.EntityAlreadyExistsError,
	handler=exceptions_user.create_exception_handler(
		status_code=status.HTTP_400_BAD_REQUEST,
		initial_detail="User already already exists.",
	),
)

app.add_exception_handler(
	exc_class_or_status_code=exceptions_user.EntityDoesNotExistError,
	handler=exceptions_user.create_exception_handler(
		status_code=status.HTTP_404_NOT_FOUND, initial_detail="User does not exist."
	),
)


app.add_exception_handler(
	exc_class_or_status_code=exceptions_user.LoginError,
	handler=exceptions_user.create_exception_handler(
		status_code=status.HTTP_401_UNAUTHORIZED, initial_detail="Invalid credentials."
	),
)


@app.get("/")
async def root():
	return {"message": "Welcoe to the User Management/Authentication API!"}
