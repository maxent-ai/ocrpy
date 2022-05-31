import os
import boto3
from dotenv import load_dotenv
from attr import define, field
from typing import List, Dict, Any
from collections import defaultdict
from ..core import AbstractTableOCR
from ..text.aws_text import aws_region_extractor

__all__ = ['AWSTableOCR']


@define
class AWSTableOCR(AbstractTableOCR):
    env_file = field(default=None)
    ocr = field(repr=False, init=False)
    mapper = field(repr=False, init=False)

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

        self.ocr = textract.analyze_document(
            Document={'Bytes': image}, FeatureTypes=["TABLES"])
        self.mapper = {b['Id']: b for b in self.ocr.get("Blocks")}

    @property
    def tables(self) -> List[List]:
        tables = [i for i in self.ocr['Blocks']
                  if i.get('BlockType') == "TABLE"]
        return [self._extract_table_data(i) for i in tables]

    def _extract_table_data(self, table):
        relationships = table['Relationships']
        if len(relationships) == 0:
            return []

        table_data = defaultdict(list)
        for i in relationships[0]['Ids']:
            cell_data = self._extract_cell(self.mapper.get(i))
            table_data[cell_data['row_index']].append(cell_data)

        return list(table_data.values())

    def _cell_text(self, cell):
        if cell.get('Relationships') is None:
            return ''

        text = []
        for rel in cell['Relationships']:
            if rel['Type'] != 'CHILD':
                continue
            for child_id in rel['Ids']:
                child = self.mapper.get(child_id)
                if child['BlockType'] == 'WORD':
                    text.append(child['Text'])
        return ' '.join(text)

    def _extract_cell(self, cell):
        text = self._cell_text(cell)
        region = aws_region_extractor(cell)
        metadata = dict(
            row_span=cell.get('RowSpan'),
            column_span=cell.get('ColumnSpan'),
            confidence=cell['Confidence'])

        return dict(text=text, row_index=cell.get('RowIndex'),
                    column_index=cell.get('ColumnIndex'), region=region, metadata=metadata)
