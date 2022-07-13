# ocrpy
[![Downloads](https://static.pepy.tech/personalized-badge/ocrpy?period=total&units=abbreviation&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/ocrpy)

Unified interface to google vision, aws textract, azure and tesseract OCR tools.


### Sample Usage

```python
from ocrpy import TextOcrPipeline

# running pipeline from pipeline config.
ocr_pipeline = TextOcrPipeline.from_config("ocrpy_config.yaml")
ocr_pipeline.process()


# alternatively you can also run a pipeline like this:
pipeline = TextOcrPipeline(source_dir='s3://document_bucket/', 
                           destination_dir="gs://processed_document_bucket/outputs/", 
                           parser_backend='aws-textract', 
                           credentials={"AWS": "path/to/aws-credentials.env/file", 
                                        "GCP": "path/to/gcp-credentials.json/file"})
pipeline.process()
```

