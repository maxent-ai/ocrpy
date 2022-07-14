Search.setIndex({"docnames": ["api", "index", "modules", "ocrpy", "ocrpy.experimental", "ocrpy.io", "ocrpy.parsers", "ocrpy.parsers.table", "ocrpy.parsers.text", "ocrpy.pipelines", "ocrpy.utils", "overview"], "filenames": ["api.rst", "index.rst", "modules.rst", "ocrpy.rst", "ocrpy.experimental.rst", "ocrpy.io.rst", "ocrpy.parsers.rst", "ocrpy.parsers.table.rst", "ocrpy.parsers.text.rst", "ocrpy.pipelines.rst", "ocrpy.utils.rst", "overview.rst"], "titles": ["API Reference", "Welcome to ocrpy\u2019s documentation", "ocrpy", "ocrpy package", "ocrpy.experimental package", "ocrpy.io package", "ocrpy.parsers package", "ocrpy.parsers.table package", "ocrpy.parsers.text package", "ocrpy.pipelines package", "ocrpy.utils package", "Overview"], "terms": {"overview": 1, "packag": [1, 2], "api": 1, "refer": 1, "index": 1, "modul": [1, 2], "search": 1, "page": [1, 8], "subpackag": 2, "experiment": [2, 3], "submodul": [2, 3], "document_classifi": [2, 3], "content": 2, "io": [2, 3, 8], "reader": [2, 3, 6, 8], "writer": [2, 3], "parser": [2, 3, 5, 10], "core": [2, 3], "pipelin": [2, 3], "config": [2, 3], "text_pipelin": [2, 3], "util": [2, 3], "except": [2, 3], "logger": [2, 3], "tabl": [3, 6], "aws_tabl": [3, 6], "table_pars": [3, 6], "text": [3, 6], "aws_text": [3, 6], "gcp_text": [3, 6], "tesseract_text": [3, 6], "text_pars": [3, 6], "class": [5, 6, 8], "documentread": [5, 8], "file": [5, 8, 10], "str": [5, 6, 8, 10], "credenti": [5, 6, 8], "option": [5, 6, 8], "none": [5, 6, 8], "base": [5, 6, 8, 10], "object": [5, 6, 8], "read": [5, 8], "an": [5, 8, 10], "imag": 5, "pdf": 5, "from": [5, 8], "local": 5, "remot": 5, "locat": 5, "note": [5, 8], "current": [5, 8], "support": [5, 8, 10], "googl": [5, 8], "storag": [5, 10], "amazon": [5, 8], "s3": 5, "The": [5, 8], "path": [5, 8], "If": 5, "aw": [5, 8], "must": [5, 8], "env": [5, 8], "format": [5, 8], "json": [5, 8], "union": 5, "gener": 5, "bytestr": 5, "return": [5, 8], "data": [5, 8], "byte": 5, "string": 5, "list": [5, 6], "storage_typ": 5, "storagewrit": 5, "write": 5, "output": 5, "given": [5, 8], "gs": 5, "default": [5, 8], "us": [5, 8, 11], "select": [5, 8], "dict": [5, 6, 8], "written": 5, "filenam": 5, "abstractblocksegment": 6, "ocr": [6, 8, 11], "ani": [6, 8], "abstract": 6, "block": [6, 10], "segment": 6, "backend": [6, 8, 10], "properti": 6, "abstractlinesegment": 6, "line": [6, 10, 11], "abstracttableocr": 6, "pars": [6, 8], "abstracttextocr": [6, 8], "awstextocr": 8, "textract": 8, "engin": [8, 11], "can": 8, "document": 8, "int": 8, "dictionari": 8, "along": 8, "addit": 8, "metadata": 8, "parsed_data": 8, "gcptextocr": 8, "cloud": 8, "vision": 8, "tesseracttextocr": 8, "pytesseract": 8, "textpars": 8, "high": 8, "level": 8, "interfac": 8, "multipl": 8, "onli": [8, 11], "name": 8, "altern": 8, "should": 8, "instanc": 8, "supported_backend": 8, "attribut": [8, 10], "valu": 8, "rais": 10, "variou": [10, 11], "attributenotsupport": 10, "when": 10, "like": 10, "extract": 10, "backendnotsupport": 10, "filetypenotsupport": 10, "process": 10, "type": 10, "guess_extens": 10, "file_path": 10, "guess": 10, "extens": 10, "guess_storag": 10, "bring": 11, "back": 11, "joi": 11, "work": 11, "python": 11, "make": 11, "easi": 11, "integr": 11, "your": 11, "exist": 11, "codebas": 11, "do": 11, "so": 11, "ad": 11, "two": 11, "code": 11}, "objects": {"ocrpy": [[5, 0, 0, "-", "io"], [10, 0, 0, "-", "utils"]], "ocrpy.io": [[5, 0, 0, "-", "reader"], [5, 0, 0, "-", "writer"]], "ocrpy.io.reader": [[5, 1, 1, "", "DocumentReader"]], "ocrpy.io.reader.DocumentReader": [[5, 2, 1, "", "credentials"], [5, 2, 1, "", "file"], [5, 3, 1, "", "read"], [5, 2, 1, "", "storage_type"]], "ocrpy.io.writer": [[5, 1, 1, "", "StorageWriter"]], "ocrpy.io.writer.StorageWriter": [[5, 2, 1, "", "credentials"], [5, 3, 1, "", "write"]], "ocrpy.parsers": [[6, 0, 0, "-", "core"], [8, 0, 0, "-", "text"]], "ocrpy.parsers.core": [[6, 1, 1, "", "AbstractBlockSegmenter"], [6, 1, 1, "", "AbstractLineSegmenter"], [6, 1, 1, "", "AbstractTableOCR"], [6, 1, 1, "", "AbstractTextOCR"]], "ocrpy.parsers.core.AbstractBlockSegmenter": [[6, 4, 1, "", "blocks"], [6, 2, 1, "", "ocr"]], "ocrpy.parsers.core.AbstractLineSegmenter": [[6, 4, 1, "", "lines"], [6, 2, 1, "", "ocr"]], "ocrpy.parsers.core.AbstractTableOCR": [[6, 2, 1, "", "credentials"], [6, 3, 1, "", "parse"]], "ocrpy.parsers.core.AbstractTextOCR": [[6, 2, 1, "", "credentials"], [6, 3, 1, "", "parse"], [6, 2, 1, "", "reader"]], "ocrpy.parsers.text": [[8, 0, 0, "-", "aws_text"], [8, 0, 0, "-", "gcp_text"], [8, 0, 0, "-", "tesseract_text"], [8, 0, 0, "-", "text_parser"]], "ocrpy.parsers.text.aws_text": [[8, 1, 1, "", "AwsTextOCR"]], "ocrpy.parsers.text.aws_text.AwsTextOCR": [[8, 3, 1, "", "parse"]], "ocrpy.parsers.text.gcp_text": [[8, 1, 1, "", "GcpTextOCR"]], "ocrpy.parsers.text.gcp_text.GcpTextOCR": [[8, 3, 1, "", "parse"]], "ocrpy.parsers.text.tesseract_text": [[8, 1, 1, "", "TesseractTextOCR"]], "ocrpy.parsers.text.tesseract_text.TesseractTextOCR": [[8, 2, 1, "", "credentials"], [8, 3, 1, "", "parse"]], "ocrpy.parsers.text.text_parser": [[8, 1, 1, "", "TextParser"]], "ocrpy.parsers.text.text_parser.TextParser": [[8, 2, 1, "", "backend"], [8, 2, 1, "", "credentials"], [8, 3, 1, "", "parse"], [8, 3, 1, "", "supported_backends"]], "ocrpy.utils": [[10, 0, 0, "-", "exceptions"], [10, 0, 0, "-", "logger"], [10, 0, 0, "-", "utils"]], "ocrpy.utils.exceptions": [[10, 5, 1, "", "AttributeNotSupported"], [10, 5, 1, "", "BackendNotSupported"], [10, 5, 1, "", "FileTypeNotSupported"]], "ocrpy.utils.utils": [[10, 6, 1, "", "guess_extension"], [10, 6, 1, "", "guess_storage"]]}, "objtypes": {"0": "py:module", "1": "py:class", "2": "py:attribute", "3": "py:method", "4": "py:property", "5": "py:exception", "6": "py:function"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "class", "Python class"], "2": ["py", "attribute", "Python attribute"], "3": ["py", "method", "Python method"], "4": ["py", "property", "Python property"], "5": ["py", "exception", "Python exception"], "6": ["py", "function", "Python function"]}, "titleterms": {"api": 0, "refer": 0, "welcom": 1, "ocrpi": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "s": 1, "document": 1, "content": [1, 3, 4, 5, 6, 7, 8, 9, 10], "indic": 1, "tabl": [1, 7], "packag": [3, 4, 5, 6, 7, 8, 9, 10], "subpackag": [3, 6], "modul": [3, 4, 5, 6, 7, 8, 9, 10], "experiment": 4, "submodul": [4, 5, 6, 7, 8, 9, 10], "document_classifi": 4, "io": 5, "reader": 5, "writer": 5, "parser": [6, 7, 8], "core": 6, "aws_tabl": 7, "table_pars": 7, "text": 8, "aws_text": 8, "gcp_text": 8, "tesseract_text": 8, "text_pars": 8, "pipelin": 9, "config": 9, "text_pipelin": 9, "util": 10, "except": 10, "logger": 10, "overview": 11}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx": 56}})