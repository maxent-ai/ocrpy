API Reference
=============

.. currentmodule:: ocrpy

``ocrpy.io``
------------
.. autoclass:: ocrpy.io.reader.DocumentReader
.. automethod:: ocrpy.io.writer.DocumentWriter.read

.. autoclass:: ocrpy.io.writer.StorageWriter
.. automethod:: ocrpy.io.writer.StorageWriter.write 

``ocrpy.parsers``
------------------

.. autoclass:: ocrpy.parsers.text.text_parser.TextParser
.. automodule:: ocrpy.parsers.text.text_parser.parse 

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

.. autoclass:: ocrpy.experimental.document_classifier.DocumentClassifier
.. automethod:: ocrpy.experimental.document_classifier.DocumentClassifier.predict


``ocrpy.utils``
---------------

.. autofunction:: ocrpy.utils.utils.guess_extension
.. autofunction:: ocrpy.utils.utils.guess_storage



