API Reference
=============

.. currentmodule:: ocrpy

``ocrpy.io``
------------

The ``ocrpy.io`` module provides utilities for reading and writing data to and from various types of storage. 
It let's you read and write Image (.png and .jpg) or Pdf files from Various types of cloud storage providers 
like Amazon S3, Google Cloud Storage, Azure Blob Storage or local file system.

These functionalities are primarily exposed through the :class:`ocrpy.io.reader.DocumentReader` 
and :class:`ocrpy.io.writer.StorageWriter` classes & they are intended to be used along with the various types of 
parsers we support which are exposed through the :class:`ocrpy.parsers.text.text_parser.TextParser` class.


.. autoclass:: ocrpy.io.reader.DocumentReader
.. automethod:: ocrpy.io.reader.DocumentReader.read

.. autoclass:: ocrpy.io.writer.StorageWriter
.. automethod:: ocrpy.io.writer.StorageWriter.write 

``ocrpy.parsers``
------------------

The ``ocrpy.parsers`` module provides a high level interface for parsing text and table from various types of documents 
with various types of backends we support. Currently, we support the following parsers: 

- :class:`ocrpy.parsers.text.text_parser.TextParser` - Parses text from various types of documents like Image, Pdf using Tesseract, Aws Textract, Azure and Google Cloud vision APIs.

- :class:`ocrpy.parsers.table.table_parser.TableParser` - Parses table from various types of documents like Image, Pdf using Aws Textract. (Table extraction with Google Cloud vision, Azure and other APIs is not supported yet - will be added soon)

.. autoclass:: ocrpy.parsers.text.text_parser.TextParser
.. automethod:: ocrpy.parsers.text.text_parser.TextParser.parse 

.. autoclass:: ocrpy.parsers.table.table_parser.TableParser
.. automethod:: ocrpy.parsers.table.table_parser.TableParser.parse

``ocrpy.parsers.text``
-----------------------

.. autoclass:: ocrpy.parsers.text.aws_text.AwsTextOCR
.. automethod:: ocrpy.parsers.text.aws_text.AwsTextOCR.parse 

.. autoclass:: ocrpy.parsers.text.gcp_text.GcpTextOCR
.. automethod:: ocrpy.parsers.text.gcp_text.GcpTextOCR.parse

.. autoclass:: ocrpy.parsers.text.tesseract_text.TesseractTextOCR
.. automethod:: ocrpy.parsers.text.tesseract_text.TesseractTextOCR.parse

``ocrpy.parsers.table``
-----------------------

.. autoclass:: ocrpy.parsers.table.aws_table.AwsTableOCR
.. automethod:: ocrpy.parsers.table.aws_table.AwsTableOCR.parse 

.. autofunction:: ocrpy.parsers.table.aws_table.table_to_csv

``ocrpy.pipelines``
-------------------

The ``ocrpy.pipelines`` module provides a set of High level classes that essentially wrap different types of 
readers, writers & parser backends and let the user do ocr on collections of documents in either remote or local 
storage and write the results to remote or local storage of their choice. 

Alternatively, it also lets the users to do ocr on document collections and index the results to a database/search 
backend of their choice.

.. autoclass:: ocrpy.pipelines.config.PipelineConfig

.. autoclass:: ocrpy.pipelines.text_pipeline.TextOcrPipeline
.. automethod:: ocrpy.pipelines.text_pipeline.TextOcrPipeline.from_config
.. autoproperty:: ocrpy.pipelines.text_pipeline.TextOcrPipeline.pipeline_config
.. automethod:: ocrpy.pipelines.text_pipeline.TextOcrPipeline.process

.. autoclass:: ocrpy.pipelines.index_pipeline.TextOcrIndexPipeline
.. automethod:: ocrpy.pipelines.index_pipeline.TextOcrIndexPipeline.from_config
.. autoproperty:: ocrpy.pipelines.index_pipeline.TextOcrIndexPipeline.pipeline_config
.. automethod:: ocrpy.pipelines.index_pipeline.TextOcrIndexPipeline.process


``ocrpy.experimental``
----------------------

The ``ocrpy.experimental`` module contains experimental features that are not yet stable and may change 
or be removed in future releases. 

Currently it exposes the :class:`ocrpy.experimental.document_classifier.DocumentClassifier` 
class which can be used to classify documents into various categories & :class:`ocrpy.experimental.layout_parser.DocumentLayoutParser` 
class which can be used to identify different components of a document like text, title, table, figures etc.

These can be used along with the ocr pipelines, as preprocessing utils to identify different types of documents
and their layout and launch appropriate ocr pipelines for custom processing.

.. autoclass:: ocrpy.experimental.document_classifier.DocumentClassifier
.. automethod:: ocrpy.experimental.document_classifier.DocumentClassifier.predict

.. autoclass:: ocrpy.experimental.layout_parser.DocumentLayoutParser
.. automethod:: ocrpy.experimental.layout_parser.DocumentLayoutParser.parse


``ocrpy.utils``
---------------

The ``ocrpy.utils`` module provides various helper functions used by the other modules in the package.

.. autofunction:: ocrpy.utils.utils.guess_extension
.. autofunction:: ocrpy.utils.utils.guess_storage



