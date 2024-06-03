from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import create_engine
from sqlalchemy import Engine
import pandas as pd
import uuid
from utils.db_helpers import use_psycopg_protocol

router = APIRouter()


class DatabaseInfo(BaseModel):
    connection_string: str = "postgres://user:password@localhost:5432/db"
    limit: int = 5


async def fetch_table_stats(engine: Engine):
    with engine.connect() as connection:
        schema_name = "public"  # TODO: create a function to determine schema name
        stats = pd.read_sql(
            f"""SELECT relname as table_name, n_live_tup as table_row_count FROM pg_stat_all_tables WHERE schemaname = '{schema_name}';""",
            con=connection,
        )
        return stats.to_dict(orient="records")


@router.post("/data/previews")
async def fetch_database_table_previews(db_info: DatabaseInfo):
    engine = create_engine(use_psycopg_protocol(db_info.connection_string))
    previews = await fetch_table_stats(engine)

    with engine.connect() as connection:
        for pos, item in enumerate(previews):
            # generate a random uuid for each table
            item["id"] = uuid.uuid4()
            table_name = item["table_name"]
            # fetch the first 5 rows of each table
            table_preview = pd.read_sql(
                f"""SELECT * FROM "{table_name}" LIMIT {db_info.limit}""", connection
            )

            previews[pos]["preview"] = table_preview.to_dict(orient="records")

    return previews
