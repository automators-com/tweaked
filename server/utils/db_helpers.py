from sqlalchemy.engine import Engine
import pandas as pd


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
