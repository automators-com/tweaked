import os
import hashlib
import tempfile
import pandas as pd
import numpy as np

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text, create_engine
from datamaker import generate_data, random_amount, random_double_precision_array
from importlib import import_module
from pathlib import Path
from server.utils.logging import logger

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

    logger.info(f"Returning table previews: {len(previews)}")
    return previews


class GenerateRequest(BaseModel):
    connection_string: str = "postgres://user:password@host:5432/db"
    quantities: int = 10
    db_schema: str


@router.post("/data/generate")
async def generate_data_from_schema(req: GenerateRequest):
    files = []
    tmp = None
    try:
        logger.info("Generating data from schema")
        engine = create_engine(use_psycopg_protocol(req.connection_string))

        with tempfile.NamedTemporaryFile(
            dir="./server", delete=True, suffix=".py"
        ) as f:
            logger.info(f"Writing schema to {f.name}")
            f.write(req.db_schema.encode())
            tmp_file_name = f.name.split("/")[-1].split(".")[0]
            schema = import_module(f"server.{tmp_file_name}")

        # generate data
        with tempfile.TemporaryDirectory(dir="./server", delete=False) as tmp:
            logger.info(f"Generating data in {tmp}")
            data_dir = Path(tmp)

            # User defined data generator functions
            custom_providers = {
                "random_amount": random_amount,
                "random_double_precision_array": random_double_precision_array,
            }

            logger.info(f"Checking schema dir: {dir(schema)}")

            data, order = generate_data(
                schema,
                quantities={},
                fallback_quantity=req.quantities,
                custom_providers=custom_providers,
                data_dir=data_dir,
            )

            # get the list of generated data files
            files = data_dir.glob("*.csv")
            # sort files according to the order of the tables
            files = sorted(files, key=lambda x: order.index(x.stem))

            # First truncate the existing tables
            with engine.connect() as conn:
                for file in files:
                    table_name = file.stem
                    logger.info(f"Truncating table: {table_name}'")
                    print(text(f'TRUNCATE "public"."{table_name}" CASCADE;'))
                    conn.execute(text(f'TRUNCATE "public"."{table_name}" CASCADE;'))

                conn.commit()

            # seed the database with the generated data
            for file in files:
                table_name = file.stem
                df = pd.read_csv(file)

                # TODO: Remove this manual fix for the client table - self relation
                if table_name == "Client":
                    df["clientId"] = None

                logger.info(f"Seeding table: {table_name}")
                df.to_sql(table_name, engine, if_exists="append", index=False)

        return {
            "success": True,
        }
    except Exception as e:
        logger.error(f"Error generating data: {e}")
        raise HTTPException(status_code=400, detail="Error generating data.")
    finally:
        for file in files:
            os.remove(file)
        os.removedirs(tmp)
        logger.info(f"Removed {f.name}")
