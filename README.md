# ocrpy
unified interface to google vision, aws textract, azure, tesseract OCR tools.

How to use
```
from ocrpy.backend import PyTesseract, AwsTextract

### PyTesseract

data = PyTesseract("image path")

### AwsTextract
data = AwsTextract("image path", env_file= "path/to/env_file")


text = data.full_text
lines = data.lines
tokens = data.tokens
blocks = data.blocks
```
sample env file for aws textract
```
region_name = region_name
aws_access_key_id = aws_access_key_id
aws_secret_access_key = aws_secret_access_key
```
