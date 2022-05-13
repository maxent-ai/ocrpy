"""
Google OCR API
"""
import cv2
import attr
from .base import Document
from google.cloud import vision
from .base import LineSegmentation
from .base import BlockSegmentation
from google.oauth2 import service_account
from ..error_handler import NotSupportedError
from ..utils import gcp_region_extractor, gcp_token_formator



@attr.s
class GCPBlockSegmentation(BlockSegmentation):
    ocr = attr.ib()

    @property
    def blocks(self):
        """
        find block form gcp response
        """
        blocks = []
        pages = self.orc.pages
        if  not isinstance(pages, list):
            pages = [pages]

        
        for page in pages:
            for block_idx, block in enumerate(page.blocks):
                vertices = block.bounding_box.vertices
                region = gcp_region_extractor(vertices)
                tokens = self._get_block_tokens(block)
                block_text = ' '.join([i.get("text") for i in tokens])
                meta_data = dict(token_count=len(tokens), text_length=len(
                    block_text), confidence= block.confidence)
                _ = dict(text=block_text, region=region, idx=block_idx, tokens=tokens, metadata=meta_data)
                blocks.append(_)

        return  blocks


    def _get_block_tokens(self, block):
        """
        get block text
        """
        tokens = []
        for para in block.paragraphs:
            for word in para.words:
                tokens.append(gcp_token_formator(word.symbols))
        return tokens


@attr.s
class GCPLineSegmentation(LineSegmentation):

    @property
    def lines(self):
        CustomError("GCP does not support line segmentation")

@attr.s
class GCPTextract(Document):
    image = attr.ib()
    env_file = attr.ib(default=None)
    ocr = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        with open(self.image, 'rb') as document:
            image = document.read()
        if self.env_file:
            cred  = service_account.Credentials.from_service_account_file(self.env_file)
            client = vision.ImageAnnotatorClient(credentials=cred)
        else:
            client = vision.ImageAnnotatorClient()
        self.ocr = client.document_text_detection(image=image).full_text_annotation


    @property
    def blocks(self):
        """
        find block form gcp response
        """
        blocks = GCPBlockSegmentation(self.ocr).blocks
        return blocks

    @property
    def lines(self):
        """
        find line form gcp response
        """
        lines = GCPLineSegmentation(self.ocr).lines
        return lines

    
    @property
    def tokens(self):
        """
        find token form gcp response
        """
        tokens = []
        for block in self.blocks:
            tokens.extend(block.get("tokens"))
        return tokens

    @property
    def full_text(self):
        """
        find full text form gcp response
        """
        return self.ocr.text
    