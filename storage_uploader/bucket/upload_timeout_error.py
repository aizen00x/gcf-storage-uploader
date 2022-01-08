class UploadTimeoutError(TimeoutError):
    def __init__(self):
        self.message = "Uploading data to Cloud Storage Bucket timed out"
