import json
from tqdm import tqdm
from attrs import define, field
from typing import Dict, Optional
from .text_pipeline import TextOcrPipeline
from haystack.document_stores import (
    OpenSearchDocumentStore,
    SQLDocumentStore,
    ElasticsearchDocumentStore,
)

__all__ = ["TextOcrIndexPipeline"]


@define
class TextOcrIndexPipeline(TextOcrPipeline):
    """
    TextOcrIndexPipeline provides a high level interface to run ocr on PDFs, JPGs, and PNGs
    in either local or cloud storage(AWS S3 or Google Cloud Storage) with a configurable parser backend
    and then index the results to a database backend of your choice.

    Note: Supported parser backends are - aws-textract, google-cloud-vision, pytesseract &
    the supported database/search backends are - sql, opensearch & elasticsearch.

    Attributes
    ----------
    database_backend : str
        The database backend to be used for indexing.
        default: "sql"
        options: "sql", "opensearch", "elasticsearch"

    database_config : dict
        A dictionary containing the credentials and other params for the database backend.
        default: None
        example: {"sql": {"db_url": "sqlite:///test.db", "db_table": "test"}}
    """

    database_backend: str = field(default="sql")
    database_config: Optional[Dict] = field(default=None)

    def _database_backend_factory(self):
        if self.database_config:
            if self.database_backend == "sql":
                return SQLDocumentStore(**self.database_config["sql"])
            elif self.database_backend == "opensearch":
                return OpenSearchDocumentStore(**self.database_config["opensearch"])
            elif self.database_backend == "elasticsearch":
                return ElasticsearchDocumentStore(**self.database_config["elasticsearch"])
            else:
                raise ValueError(f"{self.database_backend} is not a supported database backend")

    def _create_documents(self, data, file_name=None):
        full_text = " ".join([page["text"] for page_index, page in data.items()])
        return dict(content=full_text, meta=dict(file_name=file_name))

    @database_config.validator
    def _validate_credentials_config(self, attribute, value):
        if value is None:
            return
        if not isinstance(value, dict):
            raise ValueError("credentials_config must be a dictionary")
        if self.database_backend not in value:
            raise ValueError(f"credentials_config must contain a `{self.database_backend}` config")

    @property
    def pipeline_config(self):
        temp_config = self._pipeline_config()
        temp_config["database_backend"] = self.database_backend
        temp_config["database_config"] = self.database_config
        return temp_config

    def process(self):
        """
        Runs the pipeline with the given configuration and
        writes the output to the destination directory.

        Returns:
            None
        """
        batch_size = self.database_config["batch_size"]
        database_backend = self._database_backend_factory()
        docs = []

        if self.source_dir.is_dir():

            print("Running Pipeline with the following configuration:\n")
            for i, (k, v) in enumerate(self.pipeline_config.items()):
                print(f"{i+1}. {k.upper()}: {v}")

            for file in tqdm(self.source_dir.iterdir()):
                try:
                    result = self._process_file(file)
                    file_name = ".".join(file.name.split(".")[:-1])
                    file_name = f"{file_name}_{self.parser_backend}.json"
                    save_path = self.destination_dir.joinpath(file_name)
                    save_path.write_text(json.dumps(result))
                    docs.append(self._create_documents(result, file_name))

                    if len(docs) == batch_size:
                        database_backend.write_documents(docs, batch_size=batch_size)
                        docs = []

                except Exception as ex:
                    print(f"FILE: {file.name} - ERROR: {ex}")
                    continue

            if len(docs):
                database_backend.write_documents(docs)

        else:
            raise NotADirectoryError(
                """Please set the `source_dir` to the dir/bucket that has your input files and/or set the `destination_dir`
                                    to the dir/bucket where you want to write the pipeline output. """
            )
