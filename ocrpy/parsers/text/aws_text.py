import os
import time
import boto3
from dotenv import load_dotenv
from attr import define, field
from cloudpathlib import AnyPath
from ...utils.exceptions import AttributeNotSupported
from typing import List, Dict, Any, Union, Generator, ByteString
from ..core import AbstractTextOCR, AbstractLineSegmenter, AbstractBlockSegmenter

__all__ = ["AwsTextOCR"]

# TO-DO: Add logging and improve the error handling


def aws_region_extractor(block):
    x1, x2 = (
        block["Geometry"]["BoundingBox"]["Left"],
        block["Geometry"]["BoundingBox"]["Left"]
        + block["Geometry"]["BoundingBox"]["Width"],
    )
    y1, y2 = (
        block["Geometry"]["BoundingBox"]["Top"],
        block["Geometry"]["BoundingBox"]["Top"]
        + block["Geometry"]["BoundingBox"]["Height"],
    )
    return dict(x1=x1, y1=y1, x2=x2, y2=y2)


def aws_token_formator(token):
    text = token.get("Text")
    index = token.get("Id")
    region = aws_region_extractor(token)
    metadata = dict(text_length=len(text), confidence=token.get("Confidence"))
    token = dict(text=text, region=region, idx=index, metadata=metadata)
    return token


def _job_status(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    response = client.get_document_text_detection(JobId=job_id)
    while status == "IN_PROGRESS":
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
    return status


def _fetch_job_result(client, job_id):
    pages = []
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    next_token = None
    if "NextToken" in response:
        next_token = response["NextToken"]

    while next_token:
        response = client.get_document_text_detection(
            JobId=job_id, NextToken=next_token
        )
        pages.append(response)
        next_token = None
        if "NextToken" in response:
            next_token = response["NextToken"]
    return pages


@define
class AwsLineSegmenter(AbstractLineSegmenter):
    """
    Implements Line Segmentation using AWS Textract OCR Engine.
    """

    mapper = field(repr=False, init=False)

    def __attrs_post_init__(self):
        self.mapper = {i["Id"]: i for i in self.ocr["Blocks"]}

    @property
    def lines(self) -> List[Dict[str, Any]]:
        lines = []
        for line in self.ocr["Blocks"]:
            if line["BlockType"] == "LINE":

                idx = line.get("Id")
                text = line.get("Text")
                region = aws_region_extractor(line)
                tokens = self._aws_token_extractor(line.get("Relationships"))
                metadata = dict(
                    token_count=len(tokens),
                    text_length=len(text),
                    confidence=line.get("Confidence"),
                )
                line_data = dict(
                    text=text, region=region, idx=idx, tokens=tokens, metadata=metadata
                )
                lines.append(line_data)
        return lines

    def _aws_token_extractor(self, relationship):
        tokens = []
        for i in relationship:
            for idx in i.get("Ids"):
                token = self.mapper.get(idx)
                if token:
                    token = aws_token_formator(token)
                    tokens.append(token)
        return tokens


@define
class AwsBlockSegmenter(AbstractBlockSegmenter):
    @property
    def blocks(self):
        raise AttributeNotSupported(
            "AWS Backend does not support block segmentation yet."
        )


@define
class AwsTextOCR(AbstractTextOCR):
    """
    AWS Textract OCR Engine

    Attributes
    ----------
    reader: Any
        Reader object that can be used to read the document.
    credentials : str
        Path to credentials file.
        Note: The credentials file must be in .env format.
    """

    _client: boto3.client = field(repr=False, init=False)
    _document: Union[Generator, ByteString] = field(
        default=None, repr=False, init=False
    )

    def __attrs_post_init__(self):
        if self.credentials:
            load_dotenv(self.credentials)
        region = os.getenv("region_name")
        access_key = os.getenv("aws_access_key_id")
        secret_key = os.getenv("aws_secret_access_key")
        self._client = boto3.client(
            "textract",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def parse(self) -> Dict[int, Dict]:
        """
        Parses the document and returns the ocr data as a dictionary of pages along with additional metadata.

        Returns
        -------
        parsed_data : dict
            Dictionary of pages.
        """
        return self._process_data()

    def _process_data(self):
        result = {}
        ocr = self._get_ocr()
        if not isinstance(ocr, list):
            ocr = [ocr]
        for index, page in enumerate(ocr):
            data = dict(
                text=self._get_text(page),
                lines=self._get_lines(page),
                blocks=self._get_blocks(page),
                tokens=self._get_tokens(page),
            )
            result[index] = data
        return result

    def _get_ocr(self):
        storage_type = self.reader.storage_type

        if storage_type == "s3":
            path = AnyPath(self.reader.file)

            response = self._client.start_document_text_detection(
                DocumentLocation={"S3Object": {"Bucket": path.bucket, "Name": path.key}}
            )
            job_id = response["JobId"]
            status = _job_status(self.textract, job_id)
            ocr = _fetch_job_result(self.textract, job_id)

        else:
            self._document = self.reader.read()
            if isinstance(self._document, bytes):
                self._document = [self._document]
            ocr = []
            for document in self._document:
                result = self._client.detect_document_text(Document={"Bytes": document})
                ocr.append(result)
        return ocr

    def _get_blocks(self, ocr):
        try:
            return AwsBlockSegmenter(ocr).blocks
        except Exception as ex:
            return ["Error: {}".format(ex)]

    def _get_lines(self, ocr):
        try:
            return AwsLineSegmenter(ocr).lines
        except Exception as ex:
            return ["Error: {}".format(ex)]

    def _get_tokens(self, ocr):
        try:
            tokens = [
                aws_token_formator(i) for i in ocr["Blocks"] if i["BlockType"] == "WORD"
            ]
            return tokens
        except Exception as ex:
            return ["Error: {}".format(ex)]

    def _get_text(self, ocr):
        try:
            return " ".join(
                [i.get("Text") for i in ocr["Blocks"] if i.get("BlockType") == "WORD"]
            )
        except Exception as ex:
            return ["Error: {}".format(ex)]
