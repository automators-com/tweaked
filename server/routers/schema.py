import os
from pydantic import BaseModel
from fastapi import APIRouter

from server.utils.db_helpers import dump_schema

from server.utils.prompts import schema_prompt

# from server.utils.openai import client
# from server.utils.storage import upload_string_to_bucket
from server.utils.tmp import tmp_schema

router = APIRouter()


class Req(BaseModel):
    connection_string: str = "postgres://user:password@host:5432/db"


@router.post("/schema")
async def determine_schema(req: Req):
    # dump tables
    schema_dump = dump_schema(req.connection_string)

    # Use AI to generate the sqlalchemy schema
    messages = schema_prompt
    messages.append(
        {
            "role": "system",
            "content": f"Here is the pg dump output: \n{schema_dump}",
        }
    )

    # create the completion using AI
    # res = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=messages,
    # )
    # write the response to a file
    # schema = res.choices[0].message.content

    # print files in current directory

    return {"schema": tmp_schema}
