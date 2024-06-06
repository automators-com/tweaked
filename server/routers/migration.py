import os
from datetime import datetime
import json

from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from utils.db_helpers import use_psycopg_protocol
from utils.storage import (
    upload_string_to_bucket,
    list_files_in_folder,
    get_file_content_from_bucket,
)
from utils.execution_scripts import (
    call_script_in_subprocess,
    preview_exec_script,
    db_exec_script,
)

OPENAI_ORG = os.getenv("OPENAI_ORG")
OPENAI_PROJECT = os.getenv("OPENAI_PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    organization=OPENAI_ORG,
    project=OPENAI_PROJECT,
    api_key=OPENAI_API_KEY,
)

router = APIRouter()


class NewMigration(BaseModel):
    prompt: str
    preview: list[dict] | None = None
    folder: str | None = "test"


@router.post("/migrations/new")
async def generate_migration_file(req: NewMigration):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    # add context to the prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Your job is to write python functions that help users make desired modifications to their data. Provide only a simple valid python script in your response. The script should contain a function should be named 'handler'. It's only argument should be a pandas dataframe. It must return the modified pandas dataframe. The function should be written so that it works on a sample of the data as well as an entire dataset (oversample if needed). Do not write code that calls the function in your script.",
        },
        {
            "role": "system",
            "content": "Never change data column names. Never modify the shape of a dataframe. Never raise errors within the function.",
        },
    ]
    if req.preview:
        messages.append(
            {
                "role": "system",
                "content": f"Here is an sample of what the data looks like: {req.preview}",
            }
        )
    messages.append({"role": "user", "content": req.prompt})

    # create the completion using AI
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    # write the response to a file
    script = res.choices[0].message.content
    # replace the code block markdown
    script = script.replace(
        "```python\n",
        f"# prompt: {req.prompt}\n",
    ).replace("```", "")

    # upload the script to a bucket
    file_name = f"tweak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    success = upload_string_to_bucket(script, f"{req.folder}/{file_name}.py")
    print(f"File uploaded: {success}")

    # append the preview execution script
    script += preview_exec_script(req.preview)
    print(script)

    # Execute the temporary Python file in a subprocess
    result = call_script_in_subprocess(script)

    # Check for any errors
    if result.stderr:
        print("Errors from subprocess:")
        return HTTPException(status_code=400, detail=result.stderr)
    else:
        # return the updated preview
        return json.loads(result.stdout)


@router.get("/migrations/{id}")
async def get_migrations(id: str):
    # get the list of files in the folder
    files = list_files_in_folder(id)
    return files or []


class RunMigration(BaseModel):
    folder: str
    table_name: str
    connection_string: str


@router.post("/migrations/run")
async def run_migration(req: RunMigration):
    print(req)
    # get the list of migrations to run
    files = list_files_in_folder(req.folder)
    print(files)

    for file in files:
        print(file)
        # fetch the file content
        script = get_file_content_from_bucket(file)
        script += db_exec_script(
            req.table_name, use_psycopg_protocol(req.connection_string)
        )
        print(script)

        # Execute the temporary Python file in a subprocess
        result = call_script_in_subprocess(script)
        print(result)

        if "success" in result.stdout:
            continue
        else:
            return HTTPException(status_code=400, detail=result.stderr)

    return "success"
