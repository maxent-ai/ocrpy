import attr
import cv2
import pytesseract
from .base import Document
from bs4.element import Tag
from bs4 import BeautifulSoup
from .base import LineSegmentation, BlockSegmentation
from ..utils import tesseract_text_extractor, tesseract_token_extractor
from ..utils import tesseract_index_extraction, tesseract_region_extractor


@attr.s
class TesseractLineSegmentation(LineSegmentation):

    @property
    def lines(self):
        line_data = self.get_lines()
        return line_data

    def get_lines(self, block=None):
        lines = []
        if block is None:
            block = self.ocr
        for line in block.find_all('textline'):
            text = tesseract_text_extractor(line)
            region = tesseract_region_extractor(line)
            tokens = tesseract_token_extractor(line)
            index = tesseract_index_extraction(line)
            meta_data = dict(token_count=len(tokens), text_length=len(text))
            _ = dict(text=text, region=region, idx=index,
                     tokens=tokens, meta_data=meta_data)
            lines.append(_)
        return lines


@attr.s
class TesseractBlockSegmentation(BlockSegmentation):
    _line_segment = attr.ib(default=None, init=False, repr=False)

    def __attrs_post_init__(self):
        self._line_segment = TesseractLineSegmentation(self.ocr)

    @property
    def blocks(self):
        block_data = self._get_blocks()
        return block_data

    def _get_blocks(self):
        return_blocks = []
        blocks = self.ocr.find_all('textblock')
        for block in blocks:
            index = tesseract_index_extraction(block)
            text = tesseract_text_extractor(block)
            region = tesseract_region_extractor(block)
            lines = self._get_lines(block)
            tokens = tesseract_token_extractor(block)
            meta_data = dict(token_count=len(tokens),
                             line_count=len(lines), text_length=len(text))
            _ = dict(text=text, region=region, lines=lines, index=index,
                     tokens=tokens, meta_data=meta_data)
            return_blocks.append(_)
        return return_blocks

    def _get_lines(self, block):
        lines = self._line_segment.get_lines(block)
        return lines


@attr.s
class PyTesseract(Document):
    image = attr.ib()
    ocr = attr.ib(repr=False, init=False)
    ocr_xml = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        img_cv = cv2.imread(self.image)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        self.ocr = pytesseract.image_to_alto_xml(img_cv)
        self.ocr_xml = BeautifulSoup(self.ocr)

    @property
    def lines(self):
        tls = TesseractLineSegmentation(self.ocr_xml)
        lines = tls.lines
        return lines

    @property
    def blocks(self):
        tbs = TesseractBlockSegmentation(self.ocr_xml)
        blocks = tbs.blocks
        return blocks

    @property
    def tokens(self):
        token = tesseract_token_extractor(self.ocr_xml)
        return token

    @property
    def full_text(self):
        text = pytesseract.image_to_string(self.image)
        return text
