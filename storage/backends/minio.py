import logging
import io
import os
from ..storage import Storage

from minio import Minio
from minio.error import ResponseError


class MinioBackend(Storage):
    def __init__(self, logger=None):
        self.client = Minio(
            os.getenv("MINIO_URI"),
            access_key=os.getenv("MINIO_ACCESS_KEY_ID"),
            secret_key=os.getenv("MINIO_SECRET_ACCESS_KEY"),
            secure=False)
        self.logger = logger if logger else logging.getLogger("Minio")

    def get_bucket(self, bucket_name):
        return self.client.Bucket(name=bucket_name)

    def delete(self, filepath, bucket_name=None):
        try:
            self.client.remove_object(bucket_name, filepath)
            self.logger.info(
                f"Successfully deleted file {filepath} from {bucket_name}")
            return True, None
        except Exception as e:
            self.logger.error(f"Cannot delete {filepath} from {bucket_name}." +
                              f" Unexpected exception: {str(e)}")
            return False, e

    def list(self, bucket_name=None):
        try:
            self.logger.info(f"Successfully got the contents of {bucket_name}")
            return True, [obj for obj in self.client.list_objects(bucket_name)]
        except Exception as e:
            self.logger.error(f"Cannot read contents from {bucket_name}." +
                              f" Unexpected exception: {str(e)}")
            return False, e

    def read(self, filepath, bucket_name=None):
        try:
            content = self.client.get_object(bucket_name, filepath)
            self.logger.info(
                f"Successfully got the content of {filepath} to {bucket_name}")
            return True, content
        except Exception as e:
            self.logger.error(f"Cannot read {filepath} from {bucket_name}." +
                              f" Unexpected exception: {str(e)}")
            return False, e

    def save_file(self, filename, key=None, bucket_name=None):
        try:
            self.client.fput_object(bucket_name, key, filename)
            self.logger.info(f"Successfully uploaded to {bucket_name}")
            return True, None
        except Exception as e:
            self.logger.error(f"Cannot upload to {bucket_name}." +
                              f" Unexpected exception: {str(e)}")
            return False, e

    def save(self, filename, content, bucket_name=None):
        import uuid
        random_filename = str(uuid.uuid4())
        content = content.encode("utf-8")
        with open(random_filename, "wb") as f:
            f.write(content)
        self.save_file(random_filename, filename, bucket_name=bucket_name)
        os.remove(random_filename)
