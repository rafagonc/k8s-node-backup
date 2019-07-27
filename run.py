from backup import BackupController
from logger import logger
from settings import (
    BACKUP_BUCKET, BACKUP_BUCKET_BACKEND, BACKUP_CONTINUOUS, BACKUP_DIRS,
    BACKUP_EXPORTER_BACKEND, BACKUP_EXPORTER_PROMETHEUS_PUSH_GATEWAY_URI,
    BACKUP_HOSTNAME, BACKUP_INTERVAL, BACKUP_MAX_PAST_BACKUPS_ON_BUCKET,
    validate_environment_variables)

BANNER_TEXT = """
Kubernetes Node Backup v1.0.0

You can contribute to the project by adding other storage and 
metric exporter backend,fell free to open a pull 
request on https://github.com/rafagonc/k8s-node-backup

rafagonc @ 2019
"""

if __name__ == "__main__":
    print(BANNER_TEXT)
    validate_environment_variables()
    BackupController(
        dirs=BACKUP_DIRS,
        bucket_name=BACKUP_BUCKET,
        continuous=BACKUP_CONTINUOUS,
        storage_backend=BACKUP_BUCKET_BACKEND,
        exporter_backend=BACKUP_EXPORTER_BACKEND,
        exporter_uri=BACKUP_EXPORTER_PROMETHEUS_PUSH_GATEWAY_URI,
        interval=BACKUP_INTERVAL,
        hostname=BACKUP_HOSTNAME,
        max_past_backups=BACKUP_MAX_PAST_BACKUPS_ON_BUCKET,
        logger=logger).start()
