import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


from server.utils.execution_scripts import (
    call_script_in_subprocess,
    preview_query_script,
)
from server.utils.db_helpers import use_psycopg_protocol
from server.utils.prompts import query_prompt
from server.utils.openai import client
from server.utils.logging import logger

router = APIRouter()


class QueryReq(BaseModel):
    prompt: str
    connection_string: str | None = None
    table_name: str | None = None
    preview: list[dict] | None = None


@router.post("/query")
async def query_table(req: QueryReq):
    logger.info("Generating table query")
    if not req.prompt:
        logger.error("No prompt provided.")
        raise HTTPException(status_code=400, detail="A prompt is required")

    # add context to the prompt
    messages = query_prompt
    messages.append(
        {
            "role": "user",
            "content": f'My table is named: "{req.table_name}". This is what a preview of the table looks like: {req.preview}',
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

    # append the preview execution script
    script += preview_query_script(
        use_psycopg_protocol(req.connection_string), req.table_name
    )
    logger.info(f"AI created the script:\n {script}")

    # Execute the temporary Python file in a subprocess
    result = call_script_in_subprocess(script)

    # Check for any errors
    # TODO: Improve error messages
    if result.stderr:
        logger.error(result.stderr)
        # get the last line of the error
        detail = result.stderr
        if detail:
            raise HTTPException(status_code=400, detail=detail)
        else:
            raise HTTPException(
                status_code=400, detail="An error occurred while running the script."
            )
    else:
        # return the updated preview
        return json.loads(result.stdout)
