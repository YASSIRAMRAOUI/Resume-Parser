from minio import Minio as S3Minio

from src.common import MinioConfig


class Minio:
    def __init__(self, config: MinioConfig):
        self._client = S3Minio(
            endpoint=config.endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=False,
        )

    def get_object_bytes(self, bucket_name: str, object_name: str) -> bytes:
        return self._client.get_object(bucket_name, object_name).read()
