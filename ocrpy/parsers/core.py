import abc
from attr import define, field
from typing import List, Dict, Any, Optional


@define
class AbstractLineSegmenter:
    """
    Abstract class for line segmentation backends.
    """

    ocr: Any = field()

    @abc.abstractproperty
    def lines(self) -> List[Dict[str, Any]]:
        return NotImplementedError


@define
class AbstractBlockSegmenter:
    """
    Abstract class for block segmentation backends.
    """

    ocr: Any = field()

    @abc.abstractproperty
    def blocks(self) -> List[Dict[str, Any]]:
        return NotImplementedError


@define
class AbstractTextOCR:
    """
    Abstract class for Text OCR backends.
    """

    reader: Any = field()
    credentials: str = field()

    @abc.abstractmethod
    def parse(self):
        return NotImplemented


@define
class AbstractTableOCR:
    """
    Abstract class for Table OCR backends.
    """

    credentials: Optional[str] = field(default=None)

    @abc.abstractmethod
    def parse(self) -> List[List]:
        return NotImplemented
