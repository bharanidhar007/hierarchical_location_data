from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import os

from app.core.config import settings
from app.api.v1.router import api_router
from app.services.cache import init_cache

app = FastAPI(
    title=settings.PROJECT_NAME,
    default_response_class=ORJSONResponse,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_cache()

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Optional GraphQL
if settings.ENABLE_GRAPHQL:
    import strawberry
    from strawberry.asgi import GraphQL
    from app.graphql.schema import Query

    schema = strawberry.Schema(query=Query)
    app.mount("/graphql", GraphQL(schema))

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
