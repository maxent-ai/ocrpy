import attr
import cv2
import pytesseract
from ..base import Document
from bs4.element import Tag
from bs4 import BeautifulSoup
from pytesseract import Output
from ..base import LineSegmentation
from ..base import BlockSegmentation
from ...utils import tesseract_text_extractor, tesseract_token_extractor
from ...utils import tesseract_index_extraction, tesseract_region_extractor


@attr.s
class TesseractLineSegmentation(LineSegmentation):
    def __attrs_post_init__(self):
        if isinstance(self.ocr, bytes):
            self.ocr = BeautifulSoup(self.ocr)

    @property
    def lines(self):
        line_data = {}
        pages = self._get_pages()
        for page in pages:
            page_id = tesseract_index_extraction(page)
            page_height, page_width = int(
                page.get('height')), int(page.get('width'))
            lines = self.get_lines(page)
            meta_data = dict(page_id=page_id, page_height=page_height,
                             page_weight=page_width, total_lines=len(lines))
            _ = dict(lines=lines, meta_data=meta_data)
            line_data[page_id] = _
        return line_data

    def _get_pages(self):
        pages = self.ocr.find_all('page')
        return pages

    def get_lines(self, context):
        lines = []
        for line in context.find_all('textline'):
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
    _xml_format = attr.ib(default=None, init=False, repr=False)
    _line_segment = attr.ib(default=None, init=False, repr=False)

    def __attrs_post_init__(self):
        self._xml_format = BeautifulSoup(self.ocr)
        self._line_segment = TesseractLineSegmentation(self._xml_format)

    @property
    def blocks(self):
        block_data = {}
        pages = self._get_pages()
        for page in pages:
            page_id = tesseract_index_extraction(page)
            page_height, page_width = int(
                page.get('height')), int(page.get('width'))
            blocks = self._get_blocks(page)
            meta_data = dict(page_id=page_id, page_height=page_height,
                             page_weight=page_width, total_blocks=len(blocks))
            _ = dict(blocks=blocks, meta_data=meta_data)
            block_data[page_id] = _
        return block_data

    def _get_pages(self):
        pages = self._xml_format.find_all('page')
        return pages

    def _get_blocks(self, page):
        return_blocks = []
        blocks = page.find_all('textblock')
        for block in blocks:
            index = tesseract_index_extraction(block)
            text = tesseract_text_extractor(block)
            region = tesseract_region_extractor(block)
            lines = self._get_lines(block)
            tokens = tesseract_token_extractor(block)
            meta_data = dict(token_count=len(tokens),
                             line_count=len(lines), text_length=len(text))
            _ = dict(text=text, region=region, lines=lines,
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

    def __attrs_post_init__(self):
        img_cv = cv2.imread(self.image)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        self.ocr = pytesseract.image_to_alto_xml(img_cv)

    @property
    def lines(self):
        tls = TesseractLineSegmentation(self.ocr)
        lines = tls.lines
        return lines

    @property
    def blocks(self):
        tbs = TesseractBlockSegmentation(self.ocr)
        blocks = tbs.blocks
        return blocks

    @property
    def tokens(self):
        token = tesseract_token_extractor(BeautifulSoup(self.ocr))
        return token

    @property
    def full_text(self):
        text = pytesseract.image_to_string(self.image)
        return text
