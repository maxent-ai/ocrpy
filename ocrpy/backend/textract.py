import os
import attr
import uuid
import boto3
from dotenv import load_dotenv
from ..error_handler import NotSupportedError
from ..utils import aws_region_extractor, aws_token_formator
from .base import Document, LineSegmentation, BlockSegmentation


@attr.s
class TextractLineSegmentation(LineSegmentation):
    ocr = attr.ib()
    mapper = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        self.mapper = {i['Id']: i for i in self.ocr['Blocks']}

    @property
    def lines(self):
        """
        find line form aws textract response
        """

        lines = []
        for line in self.ocr["Blocks"]:
            if line["BlockType"] == "LINE":
                idx = line.get("Id")
                text = line.get("Text")
                region = aws_region_extractor(line)
                tokens = self._aws_token_extract(line.get("Relationships"))
                metadata = dict(token_count=len(tokens), text_length=len(
                    text), confidence=line.get("Confidence"))
                line_data = dict(text=text, region=region,
                                 idx=idx, tokens=tokens, metadata=metadata)
                lines.append(line_data)
        return lines

    def _aws_token_extract(self, relationship):
        """
        extract relationship from aws textract response
        """
        tokens = []
        for i in relationship:
            for idx in i.get('Ids'):
                token = self.mapper.get(idx)
                token = aws_token_formator(token)
                tokens.append(token)
        return tokens


@attr.s
class TextractBlockSegmentation(BlockSegmentation):

    @property
    def blocks(self):
        raise NotSupportedError("Aws don't support the block segmentation")


@attr.s
class AwsTextract(Document):
    image = attr.ib()
    env_file = attr.ib(default=None)
    ocr = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        with open(self.image, 'rb') as document:
            image = document.read()
        if self.env_file:
            load_dotenv(self.env_file)
        region = os.getenv('region_name')
        access_key = os.getenv('aws_access_key_id')
        secret_key = os.getenv('aws_secret_access_key')
        textract = boto3.client('textract', region_name=region,
                                aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.ocr = textract.detect_document_text(Document={'Bytes': image})

    @property
    def blocks(self):
        return TextractBlockSegmentation(self.ocr).blocks

    @property
    def lines(self):
        return TextractLineSegmentation(self.ocr).lines

    @property
    def tokens(self):
        tokens = [aws_token_formator(
            i) for i in self.ocr['Blocks'] if i['BlockType'] == 'WORD']
        return tokens

    @property
    def full_text(self):
        return ' '.join([i.get('Text') for i in self.ocr['Blocks'] if i.get('BlockType') == 'WORD'])