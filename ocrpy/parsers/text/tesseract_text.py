import cv2
import pytesseract
import numpy as np
from bs4 import BeautifulSoup
from attr import define, field
from typing import List, Dict, Any
from ..core import AbstractTextOCR, AbstractLineSegmenter, AbstractBlockSegmenter

__all__ = ["TesseractTextOCR"]

# TO-DO: Add logging and improve the error handling


def tesseract_region_extractor(context):
    x, y, w, h = (
        context.get("hpos"),
        context.get("vpos"),
        context.get("width"),
        context.get("height"),
    )
    x, y, w, h = int(x), int(y), int(w), int(h)
    x2, y2 = x + w, y + h
    return dict(x1=x, y1=y, x2=x2, y2=y2)


def tesseract_text_extractor(context):
    return_data = ""
    if context.name == "string":
        tokens = [context]
    else:
        tokens = context.find_all("string")
    token_count = len(tokens) - 1

    for index, token in enumerate(tokens):
        return_data += token.get("content")
        next_tag = token.find_next()
        if index < token_count and next_tag is not None and next_tag.name == "sp":
            return_data += " "

        if index < token_count and next_tag is not None and next_tag.name == "textline":
            return_data += "\n"

    return return_data


def tesseract_index_extraction(context):
    idx = context.get("id")
    if idx is not None:
        idx = idx.split("_")[-1]
        idx = int(idx)
    return idx


def tesseract_token_extractor(context):
    token_list = []
    for token in context.find_all("string"):
        text = token.get("content")
        region = tesseract_region_extractor(token)
        index = tesseract_index_extraction(token)
        _ = dict(
            text=text, region=region, idx=index, meta_data=dict(text_length=len(text))
        )
        token_list.append(_)
    return token_list


@define
class TesseractLineSegmenter(AbstractLineSegmenter):
    """
    Implements Line Segmentation using Tesseract OCR Engine.
    """

    @property
    def lines(self) -> List[Dict[str, Any]]:
        line_data = self._extract_lines()
        return line_data

    def _extract_lines(self, block=None) -> List[Dict[str, Any]]:
        lines = []
        if block is None:
            block = self.ocr
        for line in block.find_all("textline"):
            text = tesseract_text_extractor(line)
            region = tesseract_region_extractor(line)
            tokens = tesseract_token_extractor(line)
            index = tesseract_index_extraction(line)
            meta_data = dict(token_count=len(tokens), text_length=len(text))
            _ = dict(
                text=text, region=region, idx=index, tokens=tokens, meta_data=meta_data
            )
            lines.append(_)
        return lines


@define
class TesseractBlockSegmenter(AbstractBlockSegmenter):
    """
    Implements Block Segmentation using Tesseract OCR Engine.
    """

    @property
    def blocks(self):
        block_data = self._extract_blocks()
        return block_data

    def _extract_blocks(self):
        return_blocks = []
        blocks = self.ocr.find_all("textblock")
        line_segments = TesseractLineSegmenter(self.ocr)

        for block in blocks:
            index = tesseract_index_extraction(block)
            text = tesseract_text_extractor(block)
            region = tesseract_region_extractor(block)
            lines = line_segments._extract_lines(block)
            tokens = tesseract_token_extractor(block)
            meta_data = dict(
                token_count=len(tokens), line_count=len(lines), text_length=len(text)
            )
            _ = dict(
                text=text,
                region=region,
                lines=lines,
                index=index,
                tokens=tokens,
                meta_data=meta_data,
            )
            return_blocks.append(_)
        return return_blocks


@define
class TesseractTextOCR(AbstractTextOCR):
    """
    PyTesseract OCR Engine

    Attributes
    ----------
    reader: Any
        Reader object that can be used to read the document.
    credentials : None
        Credentials for the OCR engine (if any).
    """

    credentials: None = field(default=None)
    _document = field(default=None, repr=False, init=False)

    def __attrs_post_init__(self):
        self._document = self.reader.read()

    def parse(self):
        """
        Parses the document and returns the ocr data as a dictionary of pages along with additional metadata.

        Returns
        -------
        parsed_data : dict
            Dictionary of pages.
        """
        result = self._process_data()
        return result

    def _process_data(self):
        is_image = False
        if isinstance(self._document, bytes):
            self._document = [self._document]
            is_image = True

        result = {}
        for index, document in enumerate(self._document):
            processed_image = self._image_preprocessor(document)
            ocr = self._ocr_data(processed_image)
            data = dict(
                text=self._get_text(processed_image),
                lines=self._get_lines(ocr),
                blocks=self._get_blocks(ocr),
                tokens=self._get_tokens(ocr),
            )
            result[index] = data

        return result

        # if is_image:
        #     return result[0]
        # else:
        #     return result

    def _get_lines(self, ocr):
        tls = TesseractLineSegmenter(ocr)
        lines = tls.lines
        return lines

    def _get_blocks(self, ocr):
        tbs = TesseractBlockSegmenter(ocr)
        blocks = tbs.blocks
        return blocks

    def _get_tokens(self, ocr):
        token = tesseract_token_extractor(ocr)
        return token

    def _get_text(self, image):
        text = pytesseract.image_to_string(image)
        return text

    def _ocr_data(self, document):
        ocr = pytesseract.image_to_alto_xml(document)
        ocr_xml = BeautifulSoup(ocr, features="lxml")
        return ocr_xml

    def _image_preprocessor(self, document):
        document = np.frombuffer(document, np.uint8)
        document = cv2.imdecode(document, cv2.IMREAD_COLOR)
        document = cv2.cvtColor(document, cv2.COLOR_BGR2RGB)
        return document
