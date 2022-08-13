import io
import re
from PIL import Image
from typing import List
from attrs import define, field
from ..parsers import TextParser
from ..io.reader import DocumentReader
from layoutparser import PaddleDetectionLayoutModel

LABEL_MAP = {"PubLayNet": {0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}}


__all__ = ["DocumentLayoutParser"]


@define
class DocumentLayoutParser:

    """
    Document Layout Parser utilises a fine tuned PaddleDetection model to detect the layout of the document.
    The default model is a rcnn based model trained on the publayent dataset.

    You can also choose alternate models available on layoutparser modelshub
    at https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html

    Attributes
    ----------
    model_name : str
        The name of the model to use.
        Should be a valid model name from HuggingFace modelshub.

        default: "lp://PubLayNet/ppyolov2_r50vd_dcn_365e/config"

    Note
    ----
    - The model is trained on the Publaynet dataset and can detect the following blocks from the document:
        - text, title, list, table, figure

    - For more information on the dataset please refer this paper: https://arxiv.org/abs/1908.07836

    """

    model_name: str = field(default="lp://PubLayNet/ppyolov2_r50vd_dcn_365e/config")
    layout_parser: PaddleDetectionLayoutModel = field(default=None, init=False, repr=False)

    @model_name.validator
    def check_model_name(self, attribute, value):
        if "PubLayNet" not in value:
            raise ValueError("Currently only PubLayNet is supported")

    def __attrs_post_init__(self):
        self.layout_parser = PaddleDetectionLayoutModel(self.model_name, label_map=LABEL_MAP["PubLayNet"])

    def _bytes_to_img(self, reader):
        data = reader.read()
        if isinstance(data, bytes):
            data = [data]
        docs = []
        for page in data:
            try:
                img = Image.open(io.BytesIO(page))
                docs.append(img)
            except Exception as ex:
                print(ex)
                continue
        return docs

    def _is_overlap(self, R1, R2):
        if (R1[0] >= R2[2]) or (R1[2] <= R2[0]) or (R1[3] <= R2[1]) or (R1[1] >= R2[3]):
            return False
        else:
            return True

    def _block_formatter(self, block, tokens, meta_data):
        x1, y1, x2, y2 = (
            block.block.x_1,
            block.block.y_1,
            block.block.x_2,
            block.block.y_2,
        )
        r1 = [x1, y1, x2, y2]

        block_token = []
        for i in tokens:
            _ = i["region"]
            r2 = [_["x1"], _["y1"], _["x2"], _["y2"]]
            if meta_data:
                x1, y1, x2, y2 = r2
                x1 = x1 * meta_data["width"]
                x2 = x2 * meta_data["width"]
                y1 = y1 * meta_data["height"]
                y2 = y2 * meta_data["height"]
                r2 = [int(x1), int(y1), int(x2), int(y2)]

            if self._is_overlap(r1, r2):
                block_token.append(i)

        text = " ".join([i["text"] for i in block_token])
        text = re.sub(r"\s+", " ", text)
        region = dict(x1=x1, y1=y1, x2=x2, y2=y2)
        region = {k: round(v) for k, v in region.items()}
        meta_data = dict(
            confidence=round(block.score, 3),
            type=block.type,
            token_count=len(block_token),
            line_count=None,
            text_length=len(text),
        )
        return dict(text=text, region=region, tokens=block_token, lines=[], meta_data=meta_data)

    def _update_blocks(self, blocks, tokens, meta_data=None):
        blocks_list = []
        for block in blocks:
            blocks_list.append(self._block_formatter(block, tokens, meta_data))
        return blocks_list

    def parse(self, reader: DocumentReader, ocr: TextParser) -> List:
        """
        Predict the document type of the document in the reader.

        Parameters
        ----------
        reader : DocumentReader
            The reader containing the document to predict.


        ocr : TextParser
            The parser to use for OCR.

        Returns
        -------
        ocr_result: dict
            Blocks result of the OCR will be updated with the layout information.

        Note
        ----
        block can be following type:
        text, title, list, table, figure
        """
        ocr_result = ocr.parse(reader)
        for index, image in enumerate(self._bytes_to_img(reader)):
            meta_data = None
            if ocr.backend == "aws-textract":
                width, height = image.size
                meta_data = dict(width=width, height=height)
            layout = self.layout_parser.detect(image)
            page_ocr = ocr_result[index]
            ocr_result[index]["blocks"] = self._update_blocks(layout, page_ocr["tokens"], meta_data)

        return ocr_result
