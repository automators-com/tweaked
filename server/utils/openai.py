import os
from openai import OpenAI

OPENAI_ORG = os.getenv("OPENAI_ORG")
OPENAI_PROJECT = os.getenv("OPENAI_PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    organization=OPENAI_ORG,
    project=OPENAI_PROJECT,
    api_key=OPENAI_API_KEY,
)
