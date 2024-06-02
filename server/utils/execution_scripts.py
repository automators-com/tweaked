def preview_exec_script(preview: str):
    return f"""import json
data = pd.DataFrame({preview})
try:
    res = handler(data).to_dict(orient='records')
except Exception as e:
    res = []

print(json.dumps(res))
"""


def db_exec_script(table_name: str, connection_string: str):
    return f"""from sqlmodel import create_engine

engine = create_engine({connection_string})

with engine.connect() as connection:
    data = pd.read_sql('SELECT * FROM "{table_name}"', connection)
    try:
        df = handler(data)
        df.to_sql('{table_name}', connection, if_exists='replace', index=False)
    except Exception as e:
        print(e)
"""
