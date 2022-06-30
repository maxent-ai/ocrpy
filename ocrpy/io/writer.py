import os
import json
from attr import define, field
from dotenv import load_dotenv
from cloudpathlib import S3Client, GSClient, AnyPath

__all__ = ['DocumentWriter']


@define
class DocumentWriter:
    """
    Write a parser output to a given location (supports write to local storage, S3 and GS).
    """
    data = field()
    file = field()
    credentials = field(default=None)

    @property
    def write(self):
        client = self._get_client(self.file)
        file_data = AnyPath(self.file, client=client)
        data = self._dict_to_json(self.data)
        file_data.write_text(data)
        return None

    def _dict_to_json(self, data):
        return json.dumps(data)

    def _get_client(self, file):
        if file.startswith("gs://") and self.credentials:
            client = GSClient(application_credentials=self.credentials)

        elif file.startswith("s3://") and self.credentials:
            load_dotenv(self.credentials)
            client = S3Client(aws_access_key_id=os.getenv(
                'aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
        else:
            client = None

        return client
