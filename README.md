# ocrpy
unified interface to google vision, aws textract, azure, tesseract OCR tools.

How to use
```
from ocrpy.backend import PyTesseract
data = PyTesseract("image path")


blocks = data.blocks
lines = data.lines

```