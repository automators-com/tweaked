def use_psycopg_protocol(url: str) -> str:
    return "postgresql+psycopg://" + url.split("://")[1]


def determine_schema_name(connection_string: str) -> str:
    pass


def is_internal_table(table_name: str) -> bool:
    return table_name.startswith("_")
