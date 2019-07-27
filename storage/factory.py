from storage.backends.s3 import S3StorageBackend
from storage.backends.filesystem import FilesystemBackend
from storage.backends.minio import MinioBackend


def get_storage_backend(type="s3", logger=None):
    """
    A factory method pattern to decide which storage implementation to use

    @param: type - string (s3, filesystem)

    @return: Storage Class Implementation

    """
    if type == "s3":
        return S3StorageBackend(logger)
    elif type == "minio":
        return MinioBackend(logger)
    elif type == "filesystem":
        return FilesystemBackend(logger)
    raise NotImplementedError(
        f"No storage backend implementation for type {type}")
