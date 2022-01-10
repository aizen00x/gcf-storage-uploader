import logging
import os

from .bucket import Bucket
from .bucket import UploadTimeoutError
from .event_payload_extractor import EventPayloadExtractor
from .event_payload_extractor import DataIsNotPresentError


class StorageUploader:
    """
    Represents Google Cloud Function which is triggered by messages published to Pub/Sub topic.
    The function is responsible for extracting data from a message and uploading it to
    the Cloud Storage bucket.
    """
    def __init__(self):
        self.__bucket = Bucket()

    def process(self, event: dict) -> None:
        """
        Extract data from an event and upload it to Cloud Storage
        :param dict event: Event provided by Google Cloud when function is invoked
        :return: None
        """
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
