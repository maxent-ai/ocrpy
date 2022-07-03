from attrs import define, field
from typing import Any, Optional
from .aws_text import AwsTextOCR
from .gcp_text import GcpTextOCR
from .tesseract_text import TesseractTextOCR
from ...utils import BackendNotSupported

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
    reader : Any
        The reader object to use.
    credentials : Optional[str]
        The credentials to use for the selected backend.
        default: None
    """

    reader: Any = field()
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

    def parse(self):
        parser = self._dispatch_parser()(self.reader, self.credentials)
        parsed_doc = parser.parse()
        return parsed_doc
