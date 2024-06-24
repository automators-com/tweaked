import os
import tempfile
import subprocess
from server.utils.logging import logger


def call_script_in_subprocess(script: str):
    # Write the script to a temporary Python file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        logger.info(f"Created new tmp script: {temp_file.name}")
        temp_file.write(script.encode())
        temp_file_path = temp_file.name

    # Execute the temporary Python file in a subprocess
    command = ["python3", temp_file_path]
    logger.info(f"Executing command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)

    # Clean up the temporary file
    logger.info(f"Deleting temporary file: {temp_file_path}")
    os.remove(temp_file_path)

    return result


def preview_exec_script(preview: str):
    return f"""
import json

data = pd.DataFrame({preview})
try:
    res = handler(data.copy(deep=True)).to_dict(orient='records')
except Exception as e:
    res = data.to_dict(orient='records')

print(json.dumps(res))
"""


def preview_query_script(connection_string: str, table_name: str):
    return f"""
import json
from sqlalchemy import create_engine

engine = create_engine('{connection_string}')

try:
    df = handler(engine)
    
    # convert any timestamps to strings
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = df[col].astype(str)
    
    res = df.to_dict(orient='records')
except Exception as e:
    res = []

print(json.dumps(res))
"""


def db_exec_script(table_name: str, connection_string: str):
    return f"""
from sqlalchemy import create_engine, inspect, text
import itertools

engine = create_engine('{connection_string}')
query = 'SELECT * FROM "{table_name}";'

# fetch the entire table
with engine.connect() as connection:
    df_original = pd.read_sql(query, connection)

# apply the handler function
df_modified = handler(df_original.copy(deep=True))

# write the modified dataframe to a temporary table
df_modified.to_sql("tmp", engine, if_exists="replace", index=False)

# determine the primary key of the table
inspector = inspect(engine)
primary_key = inspector.get_pk_constraint("{table_name}").get("constrained_columns")[0]

# determine any foreign key relationships
foreign_keys = list(
    itertools.chain(
        *[
            constraint["constrained_columns"]
            for constraint in inspector.get_foreign_keys("{table_name}")
        ]
    )
)

# determine which columns were modified
modified_columns = df_original.columns[df_original.ne(df_modified).any()].tolist()

# don't update foreign or primary key columns
modified_columns = [col for col in modified_columns if col not in foreign_keys + [primary_key]]

# Update the original table with the modified data from the temp table
with engine.connect() as connection:
    transaction = connection.begin()
    for col in modified_columns:
        connection.execute(
            text(f'''UPDATE "{table_name}" {r"SET {col} = tmp.{col} FROM tmp WHERE"} "{table_name}".{r"{primary_key} = tmp.{primary_key}"}''' )
        )
    
    transaction.commit()

# Drop the tmp table
with engine.connect() as connection:
    connection.execute(text(f"DROP TABLE tmp;"))

"""
