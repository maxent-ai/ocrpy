from attrs import define, field
from ...utils import BackendNotSupported
from .aws_table import AwsTableOCR, table_to_csv
from typing import Any, Dict, Optional, Union, List

__all__ = ["TableParser"]


@define
class TableParser:
    """
    High level interface for multiple table ocr backends.
    Note: Currently only supports Amazon Textract.

    Attributes
    ----------
    backend : str
        The name of the backend to use.
        default: "aws-textract"
    credentials : str
        The credentials to use for the selected backend.
    """

    credentials: Optional[str] = field(default=None)
    backend: str = field(default="aws-textract")

    @backend.validator
    def supported_backends(self, attribute, value):
        _backends = ["aws-textract"]
        if value not in _backends:
            raise BackendNotSupported(
                f"backend type {value} not supported. choose one of these instead: {', '.join(_backends)}"
            )

    def _dispatch_parser(self):
        parser_registry = {
            "aws-textract": AwsTableOCR,
        }

        return parser_registry[self.backend]

    def parse(
        self, document: str, attempt_csv_conversion: bool = False
    ) -> Union[List, Dict]:
        """
        Parse the document and extract the tables.

        Parameters
        ----------
        document : str
            Path to the document to be parsed.
        attempt_csv_conversion : bool
            If True, attempt to convert the table to CSV.
            default: False

        Returns
        -------
        tables : Union[List, Dict]

        Note: returns a list of lists if attempt_csv_conversion is False.
        Otherwise, returns a dictionary of pandas dataframes. (each item represents an individual table in a pdf document)
        """
        parser = self._dispatch_parser()(self.credentials)
        parsed_doc = parser.parse(document)
        if attempt_csv_conversion:
            parsed_doc = table_to_csv(parsed_doc)
        return parsed_doc
