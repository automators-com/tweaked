from datetime import datetime
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.utils.db_helpers import use_psycopg_protocol
from server.utils.storage import (
    upload_string_to_bucket,
    list_files_in_folder,
    get_file_content_from_bucket,
    get_folder_name,
    delete_all_files_in_folder,
)
from server.utils.execution_scripts import (
    call_script_in_subprocess,
    preview_exec_script,
    db_exec_script,
)
from server.utils.prompts import new_tweak_prompt
from server.utils.openai import client
from server.utils.logging import logger

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
    logger.info(f"Generating tweak for {req.user_id}")
    if not req.prompt:
        logger.error(f"No prompt provided by {req.user_id}")
        raise HTTPException(status_code=400, detail="A prompt is required")

    # add context to the prompt
    messages = new_tweak_prompt
    if req.preview:
        messages.append(
            {
                "role": "system",
                "content": f"Here is an sample of what the data looks like: {req.preview}",
            }
        )
    messages.append({"role": "user", "content": req.prompt})
    logger.info(f"Tweak prompt: {req.prompt}")

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
    logger.info(f"Uploading file to {folder}/{file_name}.py")
    success = upload_string_to_bucket(script, f"{folder}/{file_name}.py")
    logger.info(f"File uploaded: {success}")

    # append the preview execution script
    script += preview_exec_script(req.preview)
    logger.info(f"AI created the script:\n {script}")

    # Execute the temporary Python file in a subprocess
    result = call_script_in_subprocess(script)

    # Check for any errors
    # TODO: Improve error messages
    if result.stderr:
        logger.error(result.stderr)
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
    logger.info(f"Fetching migrations for user {req.user_id}")
    folder = get_folder_name(req.user_id, req.connection_string, req.table_id)
    # get the list of files in the folder
    files = list_files_in_folder(folder)
    res = []

    # get the content of each file
    for file in files:
        # fetch the file content
        script = get_file_content_from_bucket(file)
        # extract the prompt from the first line
        prompt = script.split("\n")[0].replace("# prompt: ", "")
        res.append({"url": file, "prompt": prompt, "script": script})

    logger.info(f"Returning {len(res)} migrations")
    return res


class RunMigration(BaseModel):
    user_id: str
    table_id: str | None = None
    table_name: str
    connection_string: str


@router.post("/migrations/run")
async def run_migration(req: RunMigration):
    # get the list of migrations to run
    folder = get_folder_name(req.user_id, req.connection_string, req.table_id)
    files = list_files_in_folder(folder)

    for file in files:
        # fetch the file content
        script = get_file_content_from_bucket(file)
        script += db_exec_script(
            req.table_name, use_psycopg_protocol(req.connection_string)
        )

        # Execute the temporary Python file in a subprocess
        result = call_script_in_subprocess(script)

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


class DeleteMigrations(BaseModel):
    user_id: str
    connection_string: str


@router.delete("/migrations/delete/all")
async def delete_all_migrations(req: DeleteMigrations):
    logger.info(f"Deleting all migrations for user {req.user_id}")
    folder = get_folder_name(req.user_id, req.connection_string, None)
    success = delete_all_files_in_folder(folder)
    logger.info(f"Deletion success: {success}")
    return {"success": success}
