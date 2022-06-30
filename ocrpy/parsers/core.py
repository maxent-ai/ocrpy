import abc
from attr import define, field
from typing import List, Dict, Any


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

    @abc.abstractproperty
    def parse(self):
        return NotImplemented


@define
class AbstractTableOCR:
    """
    Abstract class for Table OCR backends.
    """
    document: Any = field()

    @abc.abstractproperty
    def metadata(self) -> Dict[str, Any]:
        return NotImplementedError

    @abc.abstractproperty
    def tables(self) -> List[List]:
        return NotImplemented
