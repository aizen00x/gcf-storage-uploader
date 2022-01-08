import logging
import os

from .bucket import Bucket
from .bucket import UploadTimeoutError
from .event_payload_extractor import EventPayloadExtractor
from .event_payload_extractor import DataIsNotPresentError


class StorageUploader:
    def __init__(self):
        self.__bucket = Bucket()

    def process(self, event):
        try:
            data = EventPayloadExtractor.extract(event)
            logging.info(f"Data extracted from event: {data}")

            timeout = int(os.environ.get("UPLOAD_TIMEOUT", "60"))
            self.__bucket.upload(data, timeout=timeout)
            logging.info("Data was successfully uploaded to the bucket")
        except DataIsNotPresentError as ex:
            logging.exception(ex.message)
        except UploadTimeoutError as ex:
            logging.exception(ex.message)
