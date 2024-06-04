import os
import tempfile
import subprocess


def call_script_in_subprocess(script: str):
    # Write the script to a temporary Python file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(script.encode())
        temp_file_path = temp_file.name

    # Execute the temporary Python file in a subprocess
    result = subprocess.run(
        ["../.venv/bin/python", temp_file_path], capture_output=True, text=True
    )

    # Clean up the temporary file
    os.remove(temp_file_path)

    return result


def preview_exec_script(preview: str):
    return f"""
import json

data = pd.DataFrame({preview})
try:
    res = handler(data).to_dict(orient='records')
except Exception as e:
    res = []

print(json.dumps(res))
"""


def db_exec_script(table_name: str, connection_string: str):
    return f"""
from sqlmodel import create_engine

engine = create_engine('{connection_string}')

with engine.connect() as connection:
    data = pd.read_sql('SELECT * FROM "{table_name}";', connection)
    try:
        df = handler(data)
        df.to_sql('{table_name}', connection, if_exists='replace', index=False)
        print('success')
    except Exception as e:
        print(e)
"""
