import asyncio
from contextlib import asynccontextmanager

import strawberry
from etl.kafka_etl import consume, get_consumer
from fastapi import FastAPI
from graphql_schemas.core import Mutation, Query
from routes.tasks import tasks_router
from strawberry.fastapi import GraphQLRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
	loop = asyncio.get_event_loop()
	consumer = get_consumer(loop)
	asyncio.create_task(consume(consumer))
	yield


app = FastAPI(lifespan=lifespan)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app: GraphQLRouter = GraphQLRouter(schema)

app.include_router(tasks_router)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def read_root():
	return {"Hello": "World"}
