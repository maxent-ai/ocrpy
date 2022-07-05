from attrs import define, field
from .aws_text import AwsTextOCR
from .gcp_text import GcpTextOCR
from ...io import DocumentReader
from typing import Dict, Optional
from ...utils import BackendNotSupported
from .tesseract_text import TesseractTextOCR

__all__ = ["TextParser"]


@define
class TextParser:
    """
    High level interface for multiple text ocr backends.
    Note: Currently only supports Pytesseract, Google Cloud Vision and Amazon Textract.

    Attributes
    ----------
    backend : str
        The name of the backend to use.
        default: "pytesseract"
        alternative options: "pytesseract", "aws-textract", "google-cloud-vision"
    credentials : Optional[str]
        The credentials to use for the selected backend.
        default: None
    """

    credentials: Optional[str] = field(default=None)
    backend: str = field(default="pytesseract")

    @backend.validator
    def supported_backends(self, attribute, value):
        _backends = ["pytesseract", "aws-textract", "google-cloud-vision"]
        if value not in _backends:
            raise BackendNotSupported(
                f"backend type {value} not supported. choose one of these instead: {', '.join(_backends)}"
            )

    def _dispatch_parser(self):
        parser_registry = {
            "pytesseract": TesseractTextOCR,
            "aws-textract": AwsTextOCR,
            "google-cloud-vision": GcpTextOCR,
        }

        return parser_registry[self.backend]

    def parse(self, reader: DocumentReader) -> Dict:
        """
        Parse the data from a given reader. The reader should be an instance of
        `ocrpy.io.reader.DocumentReader`.

        Parameters
        ----------
        reader : DocumentReader
            The reader to parse the data from.

        Returns
        -------
        data : Dict
            The parsed data.

        """
        parser = self._dispatch_parser()(reader, self.credentials)
        parsed_doc = parser.parse()
        return parsed_doc
