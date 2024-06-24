from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from server.utils.db_helpers import dump_schema
from server.utils.prompts import schema_prompt

# from server.utils.openai import client
# from server.utils.storage import upload_string_to_bucket
from server.utils.tmp import tmp_schema
from server.utils.logging import logger

router = APIRouter()


class Req(BaseModel):
    connection_string: str = "postgres://user:password@host:5432/db"


@router.post("/schema")
async def determine_schema(req: Req):
    logger.info(f"Generating schema for {req.connection_string}")
    # dump tables
    # try:
    #     schema_dump = dump_schema(req.connection_string)
    # except Exception as e:
    #     logger.error(f"Error pg_dumping schema: {e}")
    #     raise HTTPException(
    #         status_code=400, detail="Error extracting schema from database."
    #     )

    # Use AI to generate the sqlalchemy schema
    # messages = schema_prompt
    # messages.append(
    #     {
    #         "role": "system",
    #         "content": f"Here is the pg dump output: \n{schema_dump}",
    #     }
    # )

    # create the completion using AI
    # res = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=messages,
    # )
    # write the response to a file
    # schema = res.choices[0].message.content

    # print files in current directory

    return {"schema": tmp_schema}
