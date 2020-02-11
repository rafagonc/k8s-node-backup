import os
import socket

from exceptions import MisconfigurationException

# os.environ["BACKUP_DIR"] = os.getcwd()

BACKUP_DIRS = [
    os.environ[envvar] for envvar in os.environ
    if envvar.startswith("BACKUP_DIR")
]

BACKUP_BUCKET = os.getenv("BACKUP_BUCKET", "backups")
BACKUP_BUCKET_BACKEND = os.getenv("BACKUP_BUCKET_BACKEND", "minio")
BACKUP_EXPORTER_BACKEND = os.getenv("BACKUP_EXPORTER_BACKEND", "prometheus")
BACKUP_HOSTNAME = os.getenv("BACKUP_HOSTNAME", socket.gethostname())
BACKUP_CONTINUOUS = os.getenv("BACKUP_CONTINOUS", "true") == "true"
BACKUP_INTERVAL = int(os.getenv("BACKUP_INTERVAL", "12"))
BACKUP_MAX_PAST_BACKUPS_ON_BUCKET = int(
    os.getenv("BACKUP_MAX_PAST_BACKUPS_ON_BUCKET", "3"))
BACKUP_EXPORTER_PROMETHEUS_PUSH_GATEWAY_URI = os.getenv(
    "BACKUP_EXPORTER_PROMETHEUS_PUSH_GATEWAY_URI",
    "")


def validate_environment_variables():
    if not BACKUP_DIRS:
        raise MisconfigurationException(
            "BACKUP_DIR - Missing environment variable")

    if not BACKUP_BUCKET:
        raise MisconfigurationException(
            "BACKUP_S3_BUCKET - Missing environment variable")
