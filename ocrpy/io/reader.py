import io
import os
import pdf2image
from dotenv import load_dotenv
from attr import define, field
from cloudpathlib import S3Client, GSClient, AnyPath

__all__ = ['DocumentReader']


@define
class DocumentReader:
    """
    Read an image file from a given location and returns a byte array.
    """
    file = field()
    credentials = field(default=None)

    def read(self):
        file_type = self.get_file_type()
        if file_type == 'image':
            return self._read_image(self.file)
        elif file_type == 'pdf':
            return self._read_pdf(self.file)
        else:
            raise ValueError("File type not supported")

    def get_file_type(self):
        if self.file.endswith(".png") or self.file.endswith(".jpg"):
            file_type = "image"
        elif self.file.endswith(".pdf"):
            file_type = "pdf"
        else:
            file_type = "unknown"
        return file_type

    def get_storage_type(self):
        storage_type = None
        if self.file.startswith("gs://"):
            storage_type = 'gs'
        elif self.file.startswith("s3://"):
            storage_type = 's3'
        else:
            storage_type = 'local'
        return storage_type

    def _read_image(self, file):
        return self._read(file)

    def _read_pdf(self, file):
        data = self._read(file)
        images = self._bytes_to_images(data)
        return images

    def _read(self, file):
        client = self._get_client(file)
        file_data = AnyPath(file, client=client)
        return file_data.read_bytes()

    def _get_client(self, file):
        storage_type = self.get_storage_type()
        if storage_type == "gs" and self.credentials:
            client = GSClient(application_credentials=self.credentials)

        elif storage_type == 's3' and self.credentials:
            load_dotenv(self.credentials)
            client = S3Client(aws_access_key_id=os.getenv(
                'aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
        else:
            client = None

        return client

    def _bytes_to_images(self, data):
        images = pdf2image.convert_from_bytes(data)
        for image in images:
            buf = io.BytesIO()
            image.save(buf, format='PNG')
            yield buf.getvalue()
