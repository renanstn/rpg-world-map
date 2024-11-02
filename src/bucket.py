import os
from minio import Minio


MINIO_BUCKET_NAME = "rpg"


minio_client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)


def create_bucket_if_not_exist():
    found = minio_client.bucket_exists(MINIO_BUCKET_NAME)
    if not found:
        minio_client.make_bucket(MINIO_BUCKET_NAME)


def upload_file(file):
    object_size = os.fstat(file.fileno()).st_size
    minio_client.put_object(
        MINIO_BUCKET_NAME,
        file.filename,
        file,
        object_size,
    )


def get_minio_path(file_name):
    base_url = "localhost:9000"
    return f"http://{base_url}/{MINIO_BUCKET_NAME}/{file_name}"
