import strawberry
from fastapi import FastAPI
from graphql_schemas.core import Mutation, Query
from routes.tasks import tasks_router
from strawberry.fastapi import GraphQLRouter


app = FastAPI()

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app: GraphQLRouter = GraphQLRouter(schema)

app.include_router(tasks_router)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def read_root():
	return {"Hello": "World"}
