import os
import json
from typing import Dict, Optional
from attr import define, field
from dotenv import load_dotenv
from cloudpathlib import S3Client, GSClient, AnyPath

__all__ = ["StorageWriter"]


@define
class StorageWriter:
    """
    Write a parser output to a given location (supports write to local storage, S3 and GS).

    Attributes
    ----------
    credentials : Optional[str]
        default: None
        The credentials to use for the selected storage location.

        Note: If the storage location is AWS S3, the credentials file must be in the .env format and
        If the storage location is Google Storage, the credentials file must be in the .json format.
    """

    credentials: Optional[str] = field(default=None)

    def write(self, data: Dict, file: str) -> None:
        """
        Write the parser output to a given location (supports write to local storage, S3 and GS).

        Parameters
        ----------
        data : Dict
            The data to be written.
        file : str
            filename/path to the file to be written.

        Returns
        -------
        None
        """
        client = self._get_client(file)
        file_data = AnyPath(file, client=client)
        _data = self._dict_to_json(data)
        file_data.write_text(_data)
        return None

    def _dict_to_json(self, data):
        return json.dumps(data)

    def _get_client(self, file):
        if file.startswith("gs://") and self.credentials:
            client = GSClient(application_credentials=self.credentials)

        elif file.startswith("s3://") and self.credentials:
            load_dotenv(self.credentials)
            client = S3Client(
                aws_access_key_id=os.getenv("aws_access_key_id"),
                aws_secret_access_key=os.getenv("aws_secret_access_key"),
            )
        else:
            client = None

        return client
