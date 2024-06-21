from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import create_engine
import pandas as pd
import numpy as np
from ..utils.db_helpers import use_psycopg_protocol, fetch_table_stats, test_connection
import hashlib

router = APIRouter()


class DatabaseInfo(BaseModel):
    connection_string: str = "postgres://user:password@localhost:5432/db"
    limit: int = 5


@router.post("/data/previews")
async def fetch_database_table_previews(db_info: DatabaseInfo):
    engine = create_engine(use_psycopg_protocol(db_info.connection_string))

    message = test_connection(engine)
    if message != "ok":
        raise HTTPException(status_code=400, detail=message)

    previews = await fetch_table_stats(engine)

    with engine.connect() as connection:
        for pos, item in enumerate(previews):
            # generate a random uuid for each table
            item["id"] = hashlib.md5(item["table_name"].encode()).hexdigest()
            table_name = item["table_name"]
            # fetch the first 5 rows of each table
            table_preview = pd.read_sql(
                f"""SELECT * FROM "{table_name}" LIMIT {db_info.limit}""",
                connection,
            )

            table_preview.replace({np.nan: None}, inplace=True)
            previews[pos]["preview"] = table_preview.to_dict(orient="records")

    return previews
