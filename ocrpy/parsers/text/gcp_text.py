import numpy as np
from attr import define, field
from google.cloud import vision
from typing import List, Dict, Any
from google.oauth2 import service_account
from ...utils.errors import NotSupportedError
from ..core import AbstractTextOCR, AbstractLineSegmenter, AbstractBlockSegmenter

__all__ = ['GcpTextOCR']


def gcp_region_extractor(block):
    x_points = [v.x for v in block]
    y_points = [v.y for v in block]
    x1, x2 = min(x_points), max(x_points)
    y1, y2 = min(y_points), max(y_points)
    region = dict(x1=x1, y1=y1, x2=x2, y2=y2)
    return region


def gcp_token_formator(symbols):
    word = ''
    confidence = []
    for symbol in symbols:
        word += symbol.text
        confidence.append(symbol.confidence)
        if symbol.property.detected_break.type in (3, 5):
            word += '\n'
        elif symbol.property.detected_break.type == 4:
            word += '-'
        elif symbol.property.detected_break.type != 0:
            word += ' '

    metadata = dict(text_length=len(word), confidence=np.mean(confidence))
    word = dict(text=word,
                region=gcp_region_extractor(symbol.bounding_box.vertices),
                metadata=metadata)
    return word


@define
class GCPBlockSegmenter(AbstractBlockSegmenter):

    @property
    def blocks(self) -> List[Dict[str, Any]]:
        blocks = []
        pages = self.ocr.pages
        
        for page in pages:
            for block_idx, block in enumerate(page.blocks):
                vertices = block.bounding_box.vertices
                region = gcp_region_extractor(vertices)
                tokens = self._extract_block_tokens(block)
                block_text = ' '.join([i.get("text") for i in tokens])
                meta_data = dict(token_count=len(tokens), text_length=len(
                    block_text), confidence= block.confidence)
                _ = dict(text=block_text, region=region, idx=block_idx, tokens=tokens, metadata=meta_data)
                blocks.append(_)

        return  blocks


    def _extract_block_tokens(self, block) -> List[Dict[str, Any]]:

        tokens = []
        for para in block.paragraphs:
            for word in para.words:
                tokens.append(gcp_token_formator(word.symbols))
        return tokens


@define
class GCPLineSegmenter(AbstractLineSegmenter):

    @property
    def lines(self):
        NotSupportedError("GCP Backend does not support line segmentation yet.")

@define
class GcpTextOCR(AbstractTextOCR):
    env_file = field(default=None)
    client = field(repr=False, init=False)
    document = field(default=None, repr=False)

    def __attrs_post_init__(self):
        if self.env_file:
            cred  = service_account.Credentials.from_service_account_file(self.env_file)
            self.client = vision.ImageAnnotatorClient(credentials=cred)
        else:
            self.client = vision.ImageAnnotatorClient()

        self.document = self.reader.read()

    @property
    def parse(self):
        return self._process_data()

    def _process_data(self):
        is_image = False
        if isinstance(self.document, bytes):
            self.document = [self.document]
            is_image = True

        result = {}
        for index, document in enumerate(self.document):

            ocr = self._get_ocr(document)
            blocks = self._get_blocks(ocr)
            data = dict(text=self._get_text(ocr), lines=self._get_lines(
                ocr), blocks= blocks, tokens=self._get_tokens(blocks))
            result[index] = data

        if is_image:
            return result[0]
        else:
            return result


    def _get_blocks(self, ocr):
        try:
            return GCPBlockSegmenter(ocr).blocks
        except Exception as ex:
            return ["Error: {}".format(ex)]


    def _get_lines(self, ocr):
        try:
            return GCPLineSegmenter(ocr).lines
             
        except Exception as ex:
            return ["Error: {}".format(ex)]

    def _get_tokens(self, blocks):
        try:
            tokens = []
            for block in blocks:
                tokens.extend(block.get("tokens"))
            return tokens
        except Exception as ex:
            return ["Error: {}".format(ex)]

    def _get_text(self, ocr):
        try:
            return ocr.text
        except Exception as ex:
            return ["Error: {}".format(ex)]

    def _get_ocr(self, image):
        image = vision.types.Image(content=image)
        ocr = self.client.document_text_detection(image=image).full_text_annotation
        return ocr

    