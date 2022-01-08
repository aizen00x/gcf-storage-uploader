import logging

from storage_uploader import StorageUploader

logging.basicConfig(level=logging.INFO)


def process(event, context):
    logging.info(
        f"This function was triggered by "
        f"message id {context.event_id} published at {context.timestamp}"
    )

    StorageUploader().process(event)

