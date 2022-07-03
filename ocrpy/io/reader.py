import os
from io import BytesIO
from ..utils import LOGGER
from dotenv import load_dotenv
from attr import define, field
from pdf2image import convert_from_bytes
from ..utils import FileTypeNotSupported
from typing import Union, Generator, ByteString
from ..utils import guess_extension, guess_storage
from cloudpathlib import S3Client, GSClient, AnyPath

__all__ = ["DocumentReader"]

# TO-DO: Add logging and improve the error handling


@define
class DocumentReader:
    """
    Reads an image or a pdf file from a local or remote location.
    Note: Currently supports Google Storage and Amazon S3 Remote Files.

    Attributes
    ----------
    file : str
        The path to the file to be read.
    credentials : str
        The path to the credentials file.
        Note:
            If the Remote storage is AWS S3, the credentials file must be in the .env format.
            If the Remote storage is Google Storage, the credentials file must be in the .json format.
    """

    file: str = field()
    credentials: str = field(default=None)
    storage_type: str = field(default=None, init=False)

    def __attrs_post_init__(self):
        self.storage_type = guess_storage(self.file)

    def read(self) -> Union[Generator, ByteString]:
        """
        Reads the file from a local or remote location and
        returns the data in byte-string for an image or as a
        generator of byte-strings for a pdf.

        Returns
        -------
        data : Union[bytes, List[bytes]]
            The data in byte-string for an image or as a
            generator of byte-strings for a pdf.
        """

        file_type = guess_extension(self.file)
        reader_methods = {"IMAGE": self._read_image, "PDF": self._read_pdf}
        return (
            reader_methods[file_type](self.file)
            if file_type in reader_methods
            else FileTypeNotSupported(
                f"""We failed to understand the file type of {self.file}. The supported file-types are .png, .jpg or .pdf files. Please check the file type and try again."""
            )
        )

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
        storage_type = self.storage_type
        if storage_type == "GS" and self.credentials:
            client = GSClient(application_credentials=self.credentials)

        elif storage_type == "S3" and self.credentials:
            load_dotenv(self.credentials)
            client = S3Client(
                aws_access_key_id=os.getenv("aws_access_key_id"),
                aws_secret_access_key=os.getenv("aws_secret_access_key"),
            )
        else:
            client = None
        return client

    def _bytes_to_images(self, data):
        images = convert_from_bytes(data)
        for image in images:
            buf = BytesIO()
            image.save(buf, format="PNG")
            yield buf.getvalue()
