from attrs import define, field
from typing import Dict, Optional
from .text_pipeline import TextOcrPipeline

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

    def process(self):
        return None
