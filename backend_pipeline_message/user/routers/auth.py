from datetime import timedelta

from crud.user import user_crud
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from models.user import User
from utils.fastapi.auth.secret_key import secret_key
from utils.fastapi.auth.utils import check_password
from utils.fastapi.exceptions.exceptions_user import LoginError

auth_router = APIRouter(
	prefix="/auth",
	tags=["auth"],
)

SECRET_KEY = secret_key.secret_key

manager = LoginManager(token_url="/auth/token", secret=SECRET_KEY, use_cookie=True)
manager.cookie_name = "auth"


@manager.user_loader()
async def get_user_from_db(username: str):
	return await user_crud.get_user_by_username(username)


async def authenticate_user(username: str, password: str) -> User | None:
	user = await user_crud.get_user_by_username(username)
	if not user:
		return None
	if not check_password(password, user.hashed_password):
		return None
	return user


@auth_router.post("/token")
async def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
	user: User | None = await authenticate_user(data.username, data.password)
	if not user:
		raise LoginError(message="Invalid username or password")
	access_token_expire = timedelta(minutes=60)
	access_token = manager.create_access_token(
		data={"sub": user.username}, expires=access_token_expire
	)
	manager.set_cookie(response, token=access_token)
