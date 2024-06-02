import os
import subprocess
from datetime import datetime
import tempfile
import json

from fastapi import APIRouter
from openai import OpenAI
from pydantic import BaseModel

from utils.storage import upload_string_to_bucket
from utils.execution_scripts import preview_exec_script

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
    # add context to the prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Your job is to write python functions that help users make desired modifications to their data. Provide only a valid python script in your response. The script should contain a function should be named 'handler'. It's only argument should be a pandas dataframe. It must return the modified pandas dataframe. Do not call the function in your script.",
        },
    ]
    if req.preview:
        messages.append(
            {
                "role": "system",
                "content": f"Here is an example of what the users data looks like: {req.preview}",
            }
        )
    messages.append({"role": "user", "content": req.prompt})

    # create the completion using AI
    res = client.chat.completions.create(model="gpt-4o", messages=messages)
    # write the response to a file
    script = res.choices[0].message.content
    # replace the code block markdown
    script = script.replace(
        "```python\n",
        "",
    ).replace("```", "")

    # upload the script to a bucket
    file_name = f"tweak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    success = upload_string_to_bucket(script, f"{req.folder}/{file_name}.py")
    print(f"File uploaded: {success}")

    # append the preview execution script
    script += preview_exec_script(req.preview)
    print(script)

    # Write the script to a temporary Python file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(script.encode())
        temp_file_path = temp_file.name

    # Execute the temporary Python file in a subprocess
    result = subprocess.run(["python", temp_file_path], capture_output=True, text=True)

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Check for any errors
    if result.stderr:
        print("Errors from subprocess:")
        return result.stderr
    else:
        # return the updated preview
        return json.loads(result.stdout)
