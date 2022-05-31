import os
import boto3
from dotenv import load_dotenv
from attr import define, field
from typing import List, Dict, Any
from ...utils.errors import NotSupportedError
from ..core import AbstractTextOCR, AbstractLineSegmenter, AbstractBlockSegmenter


def aws_region_extractor(block):
    x1, x2 = block['Geometry']['BoundingBox']['Left'], block['Geometry']['BoundingBox']['Left'] + \
        block['Geometry']['BoundingBox']['Width']
    y1, y2 = block['Geometry']['BoundingBox']['Top'], block['Geometry']['BoundingBox']['Top'] + \
        block['Geometry']['BoundingBox']['Height']
    return dict(x1=x1, y1=y1, x2=x2, y2=y2)


def aws_token_formator(token):
    text = token.get("Text")
    index = token.get("Id")
    region = aws_region_extractor(token)
    metadata = dict(text_length=len(text), confidence=token.get("Confidence"))
    token = dict(text=text, region=region, idx=index, metadata=metadata)
    return token


@define
class AwsLineSegmenter(AbstractLineSegmenter):
    """
    Implements Line Segmentation using AWS Textract OCR Engine.
    """
    mapper = field(repr=False, init=False)

    def __attrs_post_init__(self):
        self.mapper = {i['Id']: i for i in self.ocr['Blocks']}

    @property
    def lines(self) -> List[Dict[str, Any]]:
        lines = []
        for line in self.ocr["Blocks"]:
            if line["BlockType"] == "LINE":
                idx = line.get("Id")
                text = line.get("Text")
                region = aws_region_extractor(line)
                tokens = self._aws_token_extractor(line.get("Relationships"))
                metadata = dict(token_count=len(tokens), text_length=len(
                    text), confidence=line.get("Confidence"))
                line_data = dict(text=text, region=region,
                                 idx=idx, tokens=tokens, metadata=metadata)
                lines.append(line_data)
        return lines

    def _aws_token_extractor(self, relationship):
        tokens = []
        for i in relationship:
            for idx in i.get('Ids'):
                token = self.mapper.get(idx)
                token = aws_token_formator(token)
                tokens.append(token)
        return tokens


@define
class AwsBlockSegmenter(AbstractBlockSegmenter):

    @property
    def blocks(self):
        raise NotSupportedError(
            "AWS Backend does not support block segmentation yet.")


@define
class AwsTextOCR(AbstractTextOCR):
    env_file = field(default=None)
    ocr = field(repr=False, init=False)

    def __attrs_post_init__(self):
        with open(self.document, 'rb') as doc:
            image = doc.read()
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
        return AwsBlockSegmenter(self.ocr).blocks

    @property
    def lines(self):
        return AwsLineSegmenter(self.ocr).lines

    @property
    def tokens(self):
        tokens = [aws_token_formator(
            i) for i in self.ocr['Blocks'] if i['BlockType'] == 'WORD']
        return tokens

    @property
    def text(self):
        return ' '.join([i.get('Text') for i in self.ocr['Blocks'] if i.get('BlockType') == 'WORD'])
