import os

from datetime import datetime
from google.cloud import storage
from .upload_timeout_error import UploadTimeoutError


class Bucket:
    """
    Establishes connection with Google Cloud Storage and is responsible for interaction with a
    bucket
    """
    def __init__(self, bucket_name: str = os.environ.get("BUCKET_NAME", "")):
        if not bucket_name:
            raise Exception("Bucket name was not provided. Pass it to the constructor or set "
                            "'BUCKET_NAME' environment variable")

        self.__bucket = storage.Client().bucket(bucket_name)

    def upload(self, data: str, timeout: int = 60) -> None:
        """
        Upload to blob from string
        :param str data: String representation of JSON data
        :param int timeout: Timeout for upload. Default is 60 seconds
        :return: None
        :raises: UploadTimeoutError
        """
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        destination_blob_name = f"{date}/{date}_{time}_covid-data.json"

        blob = self.__bucket.blob(destination_blob_name)

        try:
            blob.upload_from_string(data, timeout=timeout)
        except TimeoutError as ex:
            raise UploadTimeoutError from ex
