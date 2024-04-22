from .user import Base
from .utils.database.async_database import sessionmanager


async def create_tables():
	async with sessionmanager.engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
