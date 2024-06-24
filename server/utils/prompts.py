new_tweak_prompt = [
    {
        "role": "system",
        "content": """You are a helpful code writing assistant. Your job is to write python functions that help users make desired modifications to their data. Here are your instructions:
        - Provide only a simple valid python script in your response. 
        - The script should contain a function should be named 'handler'. 
        - The only argument to the handler function should be a pandas dataframe. 
        - The handler function should return a modified pandas dataframe. 
        - The function should be written so that it works on a sample of the data as well as an entire dataset (oversample if needed). 
        - Do not write code that calls the handler function in your script.
        - You are only allowed to import from numpy, pandas or the python standard library.
        - Never change data column names.
        - Never raise errors within the function.
        - Never modify the shape of a dataframe.
        """,
    },
    {
        "role": "user",
        "content": "Derive email from the 'name', 'surname' and 'company' columns in the dataset.",
    },
    {
        "role": "assistant",
        "content": "```python\nimport pandas as pd\n\ndef handler(df: pd.DataFrame) -> pd.DataFrame:\n    df['email'] = df['name'] + '.' + df['surname'] + '@' + df['company'] + '.com'\nreturn df\n```",
    },
]

schema_prompt = [
    {
        "role": "system",
        "content": """You are a helpful code writing assistant. Your job is to convert raw PostgresSQL pg_dump output to valid sqlalchemy schemas. Here are your instructions:
        - You shall provide a script with only the sqlalchemy code in your response . 
        - You must include a __all__ variable at the end of the script that contains all the models you have created.
        - You must import any required column datatypes from sqlalchemy.
        - You must include primary and foreign key relationships.
        - You must also make allowance for any self-referential relationships.
        - You are only allowed to import from sqlalchemy, numpy, pandas or the python standard library.
        - Never change table names, column names or casing.
        - Never raise errors within the script.
        - You must add an appropriate `info={"provider": "faker_type"}` argument to every column definition. This will be used for automatic data generation using the python faker library. Only use the faker types that are supported by the faker library.
        """,
    },
    {
        "role": "user",
        "content": """Here is the pg dump output:

CREATE TABLE public."UserOrganization" (
    id text NOT NULL,
    user_id text NOT NULL,
    org_id text NOT NULL,
    start_date timestamp(3) without time zone NOT NULL,
    end_date timestamp(3) without time zone,
    consultancy_percentage double precision DEFAULT 100 NOT NULL,
    relation text,
    country text,
    rate double precision,
    show_in_planning boolean DEFAULT true NOT NULL,
    team_lead_id text,
    is_team_lead boolean DEFAULT false NOT NULL,
    is_approved boolean DEFAULT true NOT NULL,
    role text DEFAULT 'user' NOT NULL,
    last_login timestamp(3) without time zone,
    CONSTRAINT "UserOrganization_pkey" PRIMARY KEY (id)
);

ALTER TABLE public."UserOrganization"
    ADD CONSTRAINT "UserOrganization_org_id_fkey" FOREIGN KEY (org_id) REFERENCES public."Organization" (id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public."UserOrganization"
    ADD CONSTRAINT "UserOrganization_team_lead_id_fkey" FOREIGN KEY (team_lead_id) REFERENCES public."UserOrganization" (id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE public."UserOrganization"
    ADD CONSTRAINT "UserOrganization_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User" (id) ON UPDATE CASCADE ON DELETE RESTRICT;
""",
    },
    {
        "role": "assistant",
        "content": """```python
from sqlalchemy import Column, String, DateTime, Float, Boolean, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserOrganization(Base):
    __tablename__ = 'UserOrganization'
    __table_args__ = {'schema': 'public'}

    id = Column(String, primary_key=True, nullable=False, info={"provider": "uuid4"})
    user_id = Column(String, ForeignKey('public.User.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False, info={"provider": "uuid4"})
    org_id = Column(String, ForeignKey('public.Organization.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, info={"provider": "uuid4"})
    start_date = Column(DateTime, nullable=False, info={"provider": "date_time"})
    end_date = Column(DateTime, info={"provider": "date_time"})
    consultancy_percentage = Column(Float, default=100, nullable=False, info={"provider": "pyfloat"})
    relation = Column(String, info={"provider": "word"})
    country = Column(String, info={"provider": "country"})
    rate = Column(Float, info={"provider": "pyfloat"})
    show_in_planning = Column(Boolean, default=True, nullable=False, info={"provider": "boolean"})
    team_lead_id = Column(String, ForeignKey('public.UserOrganization.id', onupdate='CASCADE', ondelete='SET NULL'), info={"provider": "uuid4"})
    is_team_lead = Column(Boolean, default=False, nullable=False, info={"provider": "boolean"})
    is_approved = Column(Boolean, default=True, nullable=False, info={"provider": "boolean"})
    role = Column(String, default='user', nullable=False, info={"provider": "enum:owner,admin,user"})
    last_login = Column(DateTime, info={"provider": "date_time"})

    user = relationship("User", back_populates="user_organizations")
    organization = relationship("Organization", back_populates="user_organizations")
    team_lead = relationship("UserOrganization", remote_side=[id])

```""",
    },
]
