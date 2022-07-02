# ocrpy
[![Downloads](https://static.pepy.tech/personalized-badge/ocrpy?period=total&units=abbreviation&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/ocrpy)

unified interface to google vision, aws textract, azure and tesseract OCR tools.


### Sample Usage

```python
from ocrpy import TextPipeline

SOURCE_DIR = 'source-dir-to-read-data'
DESTINATION_DIR = 'destination-path-to-write'

#optional: if using aws or gcp for ocr - pass the env file
#env-file need to contain `region_name`, `aws_access_key_id` and `aws_secret_access_key` vars
AWS_ENV_FILE = 'path-to-aws-credentials-env-file'
CREDENTIALS = {'aws': AWS_ENV_FILE}
PARSER_TYPE = 'aws'

ocr_pipe = TextPipeline(SOURCE_DIR, DESTINATION_DIR, PARSER_TYPE, CREDENTIALS) 
ocr_pipe.process_data()

```

