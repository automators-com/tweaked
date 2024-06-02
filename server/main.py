from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data, migration

app = FastAPI(
    title="Tweaked.ai",
    description="Fine tune your data",
    docs_url="/",
)
app.include_router(data.router, tags=["data"])
app.include_router(migration.router, tags=["migrations"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
