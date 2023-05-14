import boto3
from botocore.exceptions import ClientError
from uuid import uuid4
from starlette.config import Config
from datetime import datetime

config = Config(".env")

S3_ACCESS_KEY = config("S3_ACCESS_KEY")
S3_SECRET_KEY = config("S3_SECRET_KEY")

client_s3 = boto3.client(
    "s3", aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY
)


def upload_file(file):
    try:
        name = (
            str(uuid4())
            + "-"
            + file.filename
        )
        client_s3.upload_fileobj(
            file.file,
            "elice-8team-s3",
            name,
        )
        return name
    except ClientError as e:
        print(f"Credential error => {e}")
    except Exception as e:
        print(f"Another error => {e}")


def get_file(name):
    try:
        with open("a.jpg", "wb") as f:
            client_s3.download_fileobj("elice-8team-s3", name, f)
    except ClientError as e:
        print(f"Credential error => {e}")
    except Exception as e:
        print(f"Another error => {e}")
