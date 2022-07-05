import os
import json
import yaml
import warnings
from tqdm import tqdm
from dotenv import load_dotenv
from attr import field, define
from typing import Dict, Optional
from .config import PipelineConfig
from ..parsers import TableParser, TextParser
from ..io import DocumentReader, StorageWriter
from cloudpathlib import AnyPath, S3Client, GSClient
from ..utils import BackendNotSupported, guess_storage, guess_extension

__all__ = ["TextOcrPipeline"]

warnings.filterwarnings("ignore")


def _credentials_config_converter(value):
    if not value:
        return {"AWS": "", "GCP": ""}
    return value


@define
class TextOcrPipeline:
    """
    TextOCRPipeline provides a high level interface to run ocr on PDFs, JPGs, and PNGs
    in either local or cloud storage(AWS S3 or Google Cloud Storage) with a configurable parser backend.

    Note: Supported parser backends are - aws-textract, google-cloud-vision, pytesseract.

    Attributes
    ----------
    source_dir : str
        Path to the directory containing the documents to be processed.
    destination_dir : str
        Path to the directory where the processed documents will be stored.
    parser_backend : str
        The parser backend to be used for processing.
        default: "pytesseract"
        options: "aws-textract", "google-cloud-vision", "pytesseract"
    credentials_config : dict
        A dictionary containing the credentials for the parser or cloud storage backends.
        default: None
        example: {"AWS": "aws-credentials.env", "GCP": "gcp-credentials.json"}
    """

    source_dir: str = field()
    destination_dir: str = field()
    source_storage_type: AnyPath = field(init=False, repr=False)
    destination_storage_type: AnyPath = field(init=False, repr=False)
    parser_backend: str = field(default="pytesseract")
    credentials_config: Optional[Dict] = field(
        default=None, converter=_credentials_config_converter
    )

    def __attrs_post_init__(self):
        self.source_storage_type = guess_storage(self.source_dir)
        self.destination_storage_type = guess_storage(self.destination_dir)
        self.source_dir = AnyPath(
            self.source_dir,
            client=self._set_cloudpathlib_client(self.source_storage_type),
        )
        self.destination_dir = AnyPath(
            self.destination_dir,
            client=self._set_cloudpathlib_client(self.destination_storage_type),
        )

    @credentials_config.validator
    def _validate_credentials_config(self, attribute, value):
        if value is None:
            return
        if not isinstance(value, dict):
            raise ValueError("credentials_config must be a dictionary")
        if "AWS" not in value:
            raise ValueError("credentials_config must contain a `AWS` key")
        if "GCP" not in value:
            raise ValueError("credentials_config must contain a `GCP` key")

    @parser_backend.validator
    def _supported_backends(self, attribute, value):
        _backends = ["pytesseract", "aws-textract", "google-cloud-vision"]
        if value not in _backends:
            raise ValueError(
                f"backend type {value} not supported. choose one of these instead: {', '.join(_backends)}"
            )

    @classmethod
    def from_config(cls, config_path: str) -> "TextOcrPipeline":
        """
        Allows you to create a TextOcrPipeline from a config file (config file format: yaml).

        Parameters
        ----------
        config_path : str
            Path to the config file.

        Returns
        -------
        TextOcrPipeline
            A TextOcrPipeline object.

        Example config file:
        ---------------------
        storage_config:
            source_dir: /path/to/source/dir
            destination_dir: /path/to/destination/dir
        parser_config:
            parser_backend: pytesseract
        cloud_credentials:
            aws: /path/to/aws-credentials.env
            gcp: /path/to/gcp-credentials.json
        """
        config = PipelineConfig(config_path).pipeline_configuration
        return cls(**config)

    def _pipeline_config(self):
        """
        Provides the pipeline configuration as a dictionary.
        """
        docs = list(self.source_dir.iterdir())
        exts = [guess_extension(doc) for doc in docs]
        document_count = len(docs)
        image_file_count = len([file for file in exts if file == "IMAGE"])
        pdf_file_count = len([file for file in exts if file == "PDF"])

        return {
            "document_source": self.source_dir.name,
            "document_destination": self.destination_dir.name,
            "source_storage_type": self.source_storage_type,
            "destination_storage_type": self.destination_storage_type,
            "parser_backend_type": self.parser_backend,
            "total_document_count": document_count,
            "image_file_count": image_file_count,
            "pdf_file_count": pdf_file_count,
            "credentials": self.credentials_config,
        }

    @property
    def pipeline_config(self):
        return self._pipeline_config()

    def _set_cloudpathlib_client(self, storage_type):
        if storage_type == "GS" and self.credentials_config["GCP"]:
            client = GSClient(application_credentials=self.credentials_config["GCP"])

        elif storage_type == "S3" and self.credentials_config["AWS"]:
            load_dotenv(self.credentials_config["AWS"])
            client = S3Client(
                aws_access_key_id=os.getenv("aws_access_key_id"),
                aws_secret_access_key=os.getenv("aws_secret_access_key"),
            )
        else:
            client = None
        return client

    def _set_document_reader(self, file, source_storage_type):
        gcp_credentials = self.credentials_config["GCP"]
        aws_credentials = self.credentials_config["AWS"]

        reader_map = {
            "GS": DocumentReader(file, gcp_credentials),
            "S3": DocumentReader(file, aws_credentials),
            "LOCAL": DocumentReader(file),
        }

        return reader_map[source_storage_type]

    def _process_file(self, file):
        gcp_credentials = self.credentials_config["GCP"]
        aws_credentials = self.credentials_config["AWS"]

        reader = self._set_document_reader(file, self.source_storage_type)

        if self.parser_backend == "aws-textract":
            parser = TextParser(
                credentials=aws_credentials, backend=self.parser_backend
            )
        elif self.parser_backend == "google-cloud-vision":
            parser = TextParser(
                credentials=gcp_credentials, backend=self.parser_backend
            )
        elif self.parser_backend == "pytesseract":
            parser = TextParser(backend=self.parser_backend)
        else:
            raise ValueError(
                "Seems like the selected parser_backend or the credentials are incorrect! "
            )

        parsed_data = parser.parse(reader)
        return parsed_data

    def process(self) -> None:
        """
        Runs the pipeline with the given configuration and
        writes the output to the destination directory.

        Returns:
            None
        """
        if self.source_dir.is_dir():

            print(f"Running Pipeline with the following configuration:\n")
            for i, (k, v) in enumerate(self._pipeline_config().items()):
                print(f"{i+1}. {k.upper()}: {v}")

            for file in tqdm(self.source_dir.iterdir()):
                try:
                    result = self._process_file(file)
                    file_name = ".".join(file.name.split(".")[:-1])
                    file_name = f"{file_name}_{self.parser_backend}.json"
                    save_path = self.destination_dir.joinpath(file_name)
                    save_path.write_text(json.dumps(result))
                except Exception as ex:
                    print(f"FILE: {file.name} - ERROR: {ex}")
                    continue

        else:
            raise NotADirectoryError(
                """Please set the `source_dir` to the dir/bucket that has your input files and/or set the `destination_dir` 
                to the dir/bucket where you want to write the pipeline output. """
            )
