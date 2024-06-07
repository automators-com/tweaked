import boto3
import os
import hashlib
from botocore.client import Config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
BUCKET_ACCESS_KEY_ID = os.getenv("BUCKET_ACCESS_KEY_ID")
BUCKET_SECRET_ACCESS_KEY = os.getenv("BUCKET_SECRET_ACCESS_KEY")
BUCKET_ENDPOINT_URL = os.getenv("BUCKET_ENDPOINT_URL")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Create a session and client with the specified configuration
session = boto3.session.Session()
bucket = session.client(
    "s3",
    region_name="auto",  # R2 doesn't use region, but boto3 requires it
    endpoint_url=BUCKET_ENDPOINT_URL,
    aws_access_key_id=BUCKET_ACCESS_KEY_ID,
    aws_secret_access_key=BUCKET_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
)


def upload_string_to_bucket(file_content: str, object_name: str) -> bool:
    """Uploads a string as a file to an S3 bucket.

    Args:
        file_content (str): The string content to upload.
        object_name (str): The name of the S3 object.

    Returns:
        bool: True if the content was successfully uploaded, False otherwise.
    """
    try:
        bucket.put_object(Bucket=BUCKET_NAME, Key=object_name, Body=file_content)
    except Exception as e:
        print(e)
        return False
    return True


def get_file_content_from_bucket(object_name: str) -> str | None:
    """
    Retrieve file content from an S3 bucket and return it as a string

    Args:
        object_name (str): S3 object name

    Returns:
        str: Content of the file as a string, or None if an error occurs
    """
    try:
        response = bucket.get_object(Bucket=BUCKET_NAME, Key=object_name)
        content = response["Body"].read().decode("utf-8")
        return content
    except Exception as e:
        print(e)
        return None


def list_files_in_folder(folder_prefix):
    """List files in a specific folder of an S3 bucket.

    Args:
        bucket_name (str): Name of the bucket.
        folder_prefix (str): Prefix (folder path) to list files from.

    Returns:
        list: List of file names if successful, None otherwise.
    """
    try:
        response = bucket.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_prefix)
        files = []
        if "Contents" in response:
            for item in response["Contents"]:
                files.append(item["Key"])
        return files
    except Exception as e:
        print(e)
        return None


def get_folder_name(user_id: str, connection_string: str, table_id: str) -> str:
    # format folder structure as 'user_id/connection_string/table_name'
    hashed_con_str = hashlib.md5(connection_string.encode()).hexdigest()
    folder = f"{user_id}/{hashed_con_str}"

    # if a table id is provided, add it to the folder structure
    if table_id is not None:
        folder = f"{folder}/{table_id}"

    return folder
