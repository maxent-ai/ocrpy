import os
import boto3
import pandas as pd
from attr import define
from typing import List, Dict
from dotenv import load_dotenv
from collections import defaultdict
from ..core import AbstractTableOCR
from ..text.aws_text import aws_region_extractor

__all__ = ["AwsTableOCR", "table_to_csv"]


@define
class AwsTableOCR(AbstractTableOCR):
    """
    AWS Table Parser - This parser uses AWS Textract to analyze the document
    and extract the tables.

    Parameters
    ----------
    credentials : str
        Path to credentials file.
        Note: The credentials file must be in .env format.

    """

    def _client(self):
        if self.credentials:
            load_dotenv(self.credentials)
        region = os.getenv("region_name")
        access_key = os.getenv("aws_access_key_id")
        secret_key = os.getenv("aws_secret_access_key")
        textract = boto3.client(
            "textract",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        return textract

    def _read(self, document):
        with open(document, "rb") as doc:
            image = doc.read()
        return image

    def parse(self, document: str) -> List[List]:
        """
        Parse the document and extract the tables.

        Parameters
        ----------
        document : str
            Path to the document to be parsed.

        Returns
        -------
        tables : List[List]
            List of list of tabular data.
        """
        textract = self._client()
        image = self._read(document)
        ocr = textract.analyze_document(
            Document={"Bytes": image}, FeatureTypes=["TABLES"]
        )
        mapper = {b["Id"]: b for b in ocr.get("Blocks")}
        tables = [i for i in ocr["Blocks"] if i.get("BlockType") == "TABLE"]
        output = [self._extract_table_data(i, mapper) for i in tables]
        return output

    def _extract_table_data(self, table, mapper):
        relationships = table["Relationships"]
        if len(relationships) == 0:
            return []

        table_data = defaultdict(list)
        for i in relationships[0]["Ids"]:
            cell_data = self._extract_cell(mapper.get(i), mapper)
            table_data[cell_data["row_index"]].append(cell_data)

        return list(table_data.values())

    def _cell_text(self, cell, mapper):
        if cell.get("Relationships") is None:
            return ""

        text = []
        for rel in cell["Relationships"]:
            if rel["Type"] != "CHILD":
                continue
            for child_id in rel["Ids"]:
                child = mapper.get(child_id)
                if child["BlockType"] == "WORD":
                    text.append(child["Text"])
        return " ".join(text)

    def _extract_cell(self, cell, mapper):
        text = self._cell_text(cell, mapper)
        region = aws_region_extractor(cell)
        metadata = dict(
            row_span=cell.get("RowSpan"),
            column_span=cell.get("ColumnSpan"),
            confidence=cell["Confidence"],
        )

        return dict(
            text=text,
            row_index=cell.get("RowIndex"),
            column_index=cell.get("ColumnIndex"),
            region=region,
            metadata=metadata,
        )


def table_to_csv(table_data: List[List]) -> Dict[int, pd.DataFrame]:
    """
    Convert the table data to CSV.

    Parameters
    ----------
    table_data : List[List]
        Table data extracted from the document using the parser.

    Returns
    -------
    table_data : Dict[int, pd.DataFrame]
        Table data in CSV format.
    """
    data = {}
    for index, page in enumerate(table_data):
        df = pd.DataFrame([[j["text"] for j in i] for i in page])
        data[index] = df
    return data
