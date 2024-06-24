from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers import data, migration, updater, schema, query

app = FastAPI(
    title="Tweaked.ai",
    description="Fine tune your data",
    docs_url="/",
    version="0.0.7",
)
app.include_router(data.router, tags=["data"])
app.include_router(migration.router, tags=["migrations"])
app.include_router(updater.router, tags=["updater"])
app.include_router(schema.router, tags=["schema"])
app.include_router(query.router, tags=["query"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
