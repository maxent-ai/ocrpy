import os
import json
from dotenv import load_dotenv
from attr import field, define
from ..io import DocumentReader
from cloudpathlib import AnyPath, S3Client, GSClient
from ..parsers import TesseractTextOCR, AwsTextOCR, GcpTextOCR

__all__ = ['TextPipeline']


@define
class TextPipeline:
    source = field()
    destination = field()
    parser_type = field()  # aws, gcp, tesseract
    credentials = field(default=None)  # {'aws': , 'gcp':  }

    def __attrs_post_init__(self):
        self.source = AnyPath(
            self.source, client=self._get_client(self.source))
        self.destination = AnyPath(
            self.destination, client=self._get_client(self.destination))

    def process_data(self):
        if self.source.is_dir():
            for file in self.source.iterdir():
                try:  # To remove try catch need write file type validation code
                    result = self._process_file(file)
                    file_name = '.'.join(file.name.split(".")[:-1])
                    file_name = f"{file_name}_{self.parser_type}.json"
                    save_path = self.destination.joinpath(file_name)
                    save_path.write_text(json.dumps(result))
                except Exception as ex:
                    print(ex)
                    continue

        else:
            result = self._process_file(self.source)
            self.destination.write_text(json.dumps(result))

    def _process_file(self, file):
        reader = self._get_reader(file._str)
        if self.parser_type == 'aws':
            parser = AwsTextOCR(reader, env_file=self.credentials['aws'])

        elif self.parser_type == 'gcp':
            parser = GcpTextOCR(reader, env_file=self.credentials['gcp'])

        elif self.parser_type == 'tesseract':
            parser = TesseractTextOCR(reader)

        else:
            raise ValueError(
                "Parser type not supported, currently only 'aws', 'gcp' and 'tesseract' are supported")
        return parser.parse

    def _get_reader(self, file):
        storage_type = self._get_storage_type(file)
        if storage_type == "gs":
            reader = DocumentReader(file, self.credentials['gs'])
        elif storage_type == 's3':
            reader = DocumentReader(file, self.credentials['aws'])
        else:
            reader = DocumentReader(file)
        return reader

    def _get_client(self, file):
        storage_type = self._get_storage_type(file)
        if storage_type == "gs" and self.credentials['gcp']:
            client = GSClient(application_credentials=self.credentials['gcp'])

        elif storage_type == 's3' and self.credentials['aws']:
            load_dotenv(self.credentials['aws'])
            client = S3Client(aws_access_key_id=os.getenv(
                'aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
        else:
            client = None
        return client

    def _get_storage_type(self, path):
        storage_type = None
        if path.startswith("gs://"):
            storage_type = 'gs'
        elif path.startswith("s3://"):
            storage_type = 's3'
        else:
            storage_type = 'local'
        return storage_type
