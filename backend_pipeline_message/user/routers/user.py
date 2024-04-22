from typing import Sequence

from crud.user import user_crud
from fastapi import APIRouter, Depends
from models.user import User

from .auth import manager

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(user: User = Depends(manager)) -> Sequence[User] | User:
	if user.role.name == "admin":
		return await user_crud.get_users()
	return user
