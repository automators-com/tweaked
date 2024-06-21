from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import subprocess
from io import StringIO


def use_psycopg_protocol(url: str) -> str:
    return "postgresql+psycopg://" + url.split("://")[1]


def is_internal_table(table_name: str) -> bool:
    return table_name.startswith("_")


async def fetch_table_stats(engine: Engine):
    with engine.connect() as connection:
        schema_name = "public"  # TODO: create a function to determine schema name
        stats = pd.read_sql(
            f"""SELECT relname as table_name, n_live_tup as table_row_count FROM pg_stat_all_tables WHERE schemaname = '{schema_name}';""",
            con=connection,
        )
        return stats.to_dict(orient="records")


def test_connection(engine: Engine) -> str:
    try:
        with engine.connect():
            return "ok"
    except SQLAlchemyError as e:
        return str(e.__dict__["orig"])


def dump_schema(connection_string):
    # Construct the pg_dump command
    command = ["pg_dump", "-C", connection_string, "-s"]

    # Execute the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        raise Exception(f"Error executing pg_dump: {stderr.decode('utf-8')}")

    # Filter out the CREATE TABLE statement for the specific table
    statements = []
    capturing = False
    for line in StringIO(stdout.decode("utf-8")):
        if capturing:
            statements.append(line.strip())
            if line.strip().endswith(";"):
                capturing = False
        elif line.strip().startswith("CREATE TABLE"):
            capturing = True
            statements.append(line.strip())

    # Return the CREATE TABLE statements as a single string
    return "\n".join(statements)
