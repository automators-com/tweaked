from pydantic import BaseModel
from fastapi import APIRouter
from sqlalchemy import create_engine, MetaData
from utils.db_helpers import use_psycopg_protocol

router = APIRouter()


class Req(BaseModel):
    connection_string: str = "postgres://user:password@localhost:5432/db"


@router.post("/schema")
async def determine_schema(req: Req):
    # Create SQLAlchemy engine
    engine = create_engine(use_psycopg_protocol(req.connection_string))

    # Create MetaData object
    metadata = MetaData()

    # Reflect the schema from the database
    metadata.reflect(bind=engine)

    # Write the reflected schema to a Python file
    f: str = ""

    f += "from sqlalchemy import Column\n"
    f += "from sqlalchemy.ext.declarative import declarative_base\n"
    f += "Base = declarative_base()\n\n"

    for table in metadata.sorted_tables:
        f += f"class {table.name.capitalize()}(Base):\n"
        f += f"    __tablename__ = '{table.name}'\n\n"
        for column in table.columns:
            f += f"    {column.name} = Column('{str(column.type)}')\n"
        f += "\n"

    with open("schema_test.py", "w") as file:
        file.write(f)

    return "file written successfully"
