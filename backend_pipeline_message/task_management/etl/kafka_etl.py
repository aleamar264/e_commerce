import json

from aiokafka import AIOKafkaConsumer
from model.tasks import User
from schemas.user import User as user_schema
from utils.database.async_database import sessionmanager


async def etl(msg):
	payload: dict = json.loads(msg.value)
	__data: dict[str, str] = {
		"op": payload.pop("__op"),
		"deleted": payload.pop("__deleted"),
	}
	user = user_schema(
		id=payload.pop("id"),
		is_active=payload.pop("is_active"),
		role=payload.pop("role"),
		username=payload.pop("username"),
	)
	async with sessionmanager.async_session() as session:
		if __data["op"] == "c":
			user_: User = User(**user.model_dump())
			session.add(user_)
			await session.commit()
			await session.refresh(user_)


kafka_actions = {
	"user_changes.public.user": etl,
}


async def consume(consumer: AIOKafkaConsumer):
	try:
		await consumer.start()
	except Exception as e:
		print(e)
		return
	try:
		async for msg in consumer:
			await kafka_actions[msg.topic](msg)
	finally:
		await consumer.stop()


consumer_config = {"group_id": "my-fastapi-consumer", "auto_offset_reset": "earliest"}


def get_consumer(loop):
	return AIOKafkaConsumer(
		"user_changes.public.user",
		loop=loop,
		bootstrap_servers="broker:29092",
		*consumer_config,
	)
