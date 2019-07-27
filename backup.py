import os
import random
import string
import zipfile
import datetime
import socket
import pause

from timer import Timer
from storage.factory import get_storage_backend
from exporters.factory import get_exporter_backend
from console_progressbar import ProgressBar


class BackupController():
    def __init__(self,
                 dirs,
                 bucket_name,
                 continuous,
                 logger,
                 storage_backend="minio",
                 exporter_backend="prometheus",
                 max_past_backups=5,
                 interval=12,
                 exporter_uri=None,
                 hostname=socket.gethostname()):
        self.dirs = dirs
        self.bucket_name = bucket_name
        self.continuous = continuous
        self.max_past_backups = max_past_backups
        self.hostname = hostname
        self.interval = interval
        self.storage = get_storage_backend(type=storage_backend, logger=logger)
        self.exporter = get_exporter_backend(
            exporter_uri, type=exporter_backend, logger=logger)
        self.logger = logger

    def random_string(self,
                      size=3,
                      chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def zipit(self, folders, dst):

        pb = ProgressBar(
            total=100,
            prefix='Zip Progress',
            suffix='Completed',
            decimals=2,
            length=50,
            fill='>',
            zfill='-')
        count = 0
        progress = 0

        self.logger.info("Counting Files...")

        zip_file = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
        for folder in folders:
            for dirpath, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    count += 1

        self.logger.info("%s files found to be zipped" % count)

        for folder in folders:
            for dirpath, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    zip_file.write(
                        os.path.join(dirpath, filename),
                        os.path.relpath(
                            os.path.join(dirpath, filename),
                            os.path.join(folders[0], '../..')))
                    progress += 1
                    pb.print_progress_bar((progress / count) * 100)

        zip_file.close()

    def generate_filename(self, ):
        return datetime.date.today().strftime(
            "%Y-%m-%d") + "-" + self.hostname + "_" + self.random_string(
            ) + ".zip"

    def delete_past_backups(self):
        self.logger.info(
            "Checking past backups from bucket %s" % (self.bucket_name))
        past_backups = [
            (obj.object_name, obj.last_modified)
            for obj in self.storage.list(bucket_name=self.bucket_name)[1]
        ]
        past_backups.sort(key=lambda tup: tup[1], reverse=False)
        if len(past_backups) > self.max_past_backups:
            for key, date in past_backups[0:(
                    len(past_backups) - self.max_past_backups)]:
                self.storage.delete(key, bucket_name=self.bucket_name)
                self.logger.info(
                    "Deleted past backup with key %s and last modified date %s"
                    % (key, date))

    def export_compression_timer(self, t):
        self.exporter.export(
            metric_name="node_backup_zip_compression_time",
            metric_value=t.interval,
            metric_description="Total time spent " + "zipping backup folders",
            labels={"hostname": self.hostname})

    def export_upload_timer(self, t):
        self.exporter.export(
            metric_name="node_backup_upload_time",
            metric_value=t.interval,
            metric_description="Total time spent " + "uploading backup file",
            labels={"hostname": self.hostname})

    def export_backup_file_size(self, filename):
        size = os.path.getsize(filename)
        self.exporter.export(
            metric_name="node_backup_backup_file_size_in_bytes",
            metric_value=size,
            metric_description="File size of backup file" + " in bytes",
            labels={"hostname": self.hostname})

    def start(self):
        while self.continuous:
            self.delete_past_backups()

            self.logger.info("Doing cluster backup at %s for %s" %
                             (datetime.date.today(), self.hostname))
            filename = self.generate_filename()

            self.logger.info("Starting to zip dirs named %s..." % (self.dirs))

            with Timer() as compression_elapsed_time:
                self.zipit(self.dirs, filename)
                compression_elapsed_time.end_timer()
                self.export_compression_timer(compression_elapsed_time)
                self.export_backup_file_size(filename)

            self.logger.info("Successfully zipped dirs named %s" % (self.dirs))
            self.logger.info("Uploading zipped file %s" % filename)

            if self.bucket_name:
                with Timer() as upload_elapsed_time:
                    self.storage.save_file(
                        filename, key=filename, bucket_name=self.bucket_name)
                    upload_elapsed_time.end_timer()
                    self.export_upload_timer(upload_elapsed_time)
                    self.logger.info("Sucessfully uploaded %s" % filename)
            else:
                self.logger.info("No bucket specified")

            self.logger.info("Waiting 12 hours to backup again...")
            pause.hours(self.interval)
