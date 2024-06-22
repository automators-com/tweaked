import os
from datetime import datetime
import json

from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from ..utils.db_helpers import use_psycopg_protocol
from ..utils.storage import (
    upload_string_to_bucket,
    list_files_in_folder,
    get_file_content_from_bucket,
    get_folder_name,
)
from ..utils.execution_scripts import (
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
    user_id: str | None = None
    connection_string: str | None = None
    table_id: str | None = None
    folder: str | None = "test"


@router.post("/migrations/new")
async def generate_migration_file(req: NewMigration):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="A prompt is required")

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

    # create a unique file name - this can be easily ordered
    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    folder = get_folder_name(req.user_id, req.connection_string, req.table_id)

    # upload the script to a bucket
    success = upload_string_to_bucket(script, f"{folder}/{file_name}.py")
    print(f"File uploaded: {success}")

    # append the preview execution script
    script += preview_exec_script(req.preview)
    print(script)

    # Execute the temporary Python file in a subprocess
    result = call_script_in_subprocess(script)

    # Check for any errors
    # TODO: Improve error messages
    if result.stderr:
        print("Errors from subprocess:")
        print(result.stderr)
        # get the last line of the error
        detail = result.stderr.split("\n")[-2]
        if detail:
            raise HTTPException(status_code=400, detail=detail)
        else:
            raise HTTPException(
                status_code=400, detail="An error occurred while running the script."
            )
    else:
        # return the updated preview
        return json.loads(result.stdout)


class FetchMigrations(BaseModel):
    user_id: str
    connection_string: str
    table_id: str


@router.post("/migrations/list")
async def get_migrations(req: FetchMigrations):
    folder = get_folder_name(req.user_id, req.connection_string, req.table_id)
    # get the list of files in the folder
    files = list_files_in_folder(folder)
    print(files)
    res = []

    # get the content of each file
    for file in files:
        # fetch the file content
        script = get_file_content_from_bucket(file)
        # extract the prompt from the first line
        prompt = script.split("\n")[0].replace("# prompt: ", "")
        print(script)
        res.append({"url": file, "prompt": prompt, "script": script})

    return res


class RunMigration(BaseModel):
    user_id: str
    table_id: str | None = None
    table_name: str
    connection_string: str


@router.post("/migrations/run")
async def run_migration(req: RunMigration):
    print(req)
    # get the list of migrations to run
    folder = get_folder_name(req.user_id, req.connection_string, req.table_id)
    files = list_files_in_folder(folder)
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
            detail = result.stderr.split("\n")[-2]
            if detail:
                raise HTTPException(status_code=400, detail=detail)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="An error occurred while running the script.",
                )

    return "success"
