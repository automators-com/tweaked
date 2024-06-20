from pydantic import BaseModel
from fastapi import APIRouter
from omymodels import create_models
from ..utils.db_helpers import dump_schema
from ..utils.storage import upload_string_to_bucket

router = APIRouter()


class Req(BaseModel):
    connection_string: str = "postgres://user:password@localhost:5432/db"


@router.post("/schema")
async def determine_schema(req: Req):
    # dump tables
    schema = dump_schema(req.connection_string)

    # parse and construct sqlalchemy models
    models = create_models(schema, models_type="sqlalchemy")["code"]
    # small fixes to models
    models = models.replace("double precision()", "sa.DOUBLE_PRECISION()")
    models = models.replace("::text", "")

    with open("schema_out.py", "w") as f:
        f.write(models)

    # upload schema to R2
    upload_string_to_bucket(models, "schema_out.py")

    # Print or use the schema string as needed
    print(models)

    return models
