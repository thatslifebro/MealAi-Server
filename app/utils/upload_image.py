import boto3
from botocore.exceptions import ClientError
from starlette.config import Config

config = Config(".env")

S3_ACCESS_KEY = config("S3_ACCESS_KEY")
S3_SECRET_KEY = config("S3_SECRET_KEY")

client_s3 = boto3.client(
    "s3", aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY
)


def upload_file(file):
    try:
        client_s3.upload_fileobj(
            file.file,
            "elice-8team-s3",
            file.filename,
        )
        return file.filename
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
