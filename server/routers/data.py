import hashlib
import tempfile
import pandas as pd
import numpy as np

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text, create_engine
from datamaker import generate_data
from importlib import import_module
from pathlib import Path

from server.utils.db_helpers import (
    use_psycopg_protocol,
    fetch_table_stats,
    test_connection,
)

router = APIRouter()


class DatabaseInfo(BaseModel):
    connection_string: str = "postgres://user:password@host:5432/db"
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


class GenerateRequest(BaseModel):
    connection_string: str = "postgres://user:password@host:5432/db"
    quantities: int = 10
    db_schema: str


@router.post("/data/generate")
async def generate_data_from_schema(req: GenerateRequest):
    print("Generating data from schema")
    engine = create_engine(use_psycopg_protocol(req.connection_string))

    # create a tmp folder in the current working directory

    with tempfile.NamedTemporaryFile(dir="./server", delete=True, suffix=".py") as f:
        f.write(req.db_schema.encode())
        print(f"server.{f.name}")
        tmp_file_name = f.name.split("/")[-1].split(".")[0]
        schema = import_module(f"server.{tmp_file_name}")

    # generate data
    with tempfile.TemporaryDirectory(dir="./server", delete=False) as tmp:
        data_dir = Path(tmp)

        data, order = generate_data(
            schema,
            quantities={},
            fallback_quantity=req.quantities,
            custom_providers={},
            data_dir=data_dir,
        )

        # get the list of generated data files
        files = data_dir.glob("*.csv")
        # sort files according to the order of the tables
        files = sorted(files, key=lambda x: order.index(x.stem))

        # First truncate the existing table
        with engine.connect() as conn:
            for file in files:
                table_name = file.stem
                conn.execute(text(f'TRUNCATE "{table_name}" CASCADE;'))

        # seed the database with the generated data
        for file in files:
            table_name = file.stem
            df = pd.read_csv(file)

            # Manual fix for the client table
            if table_name == "Client":
                df["clientId"] = None

            df.to_sql(table_name, engine, if_exists="append", index=False)

    return "success"
