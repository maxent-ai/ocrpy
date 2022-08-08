Examples 
========

Weather you are working with images or pdfs, you can use ``ocrpy`` to extract text or tables from them, 
further you can also classify a document automatically as an invoice, research-paper or any other document and process them accordingly.
with various types of parsers (cloud/open-source) and classifiers available. 

Ocrpy let's you do most of the things with just few lines of code! 
Here are some examples on using ocrpy at different levels of abstraction.

text extraction with ``ocrpy.pipelines``
----------------------------------------

First let's use ocrpy from it's hightest level of abstraction, which is the ``ocrpy.pipelines`` API. 

The Pipeline API can be invoked in two ways. The first method is to define the config for running the 
pipeline as a yaml file and and then run the pipeline by loading it as follows: 

.. code-block:: python

   from ocrpy import TextOcrPipeline
   
   PIPELINE_CONFIG_PATH = "ocrpy_config.yaml" # path to the pipeline config file
   ocr_pipeline = TextOcrPipeline.from_config(PIPELINE_CONFIG_PATH)
   ocr_pipeline.process()

alternatively you can also run a pipeline by directly instantiating the pipeline class as follows:

.. code-block:: python

   from ocrpy import TextOcrPipeline

   SOURCE = 's3://document_bucket/' # s3 bucket or local directory or gcs bucket with your documents.
   DESTINATION = 'gs://processed_document_bucket/outputs/' # s3 bucket or local directory or gcs bucket to write the processed documents.
   PARSER = 'aws-textract' # or 'google-cloud-vision' or 'pytesseract'
   CREDENTIALS = {"AWS": "path/to/aws-credentials.env/file", 
                  "GCP": "path/to/gcp-credentials.json/file"} # optional - if you are using any cloud service.

   pipeline = TextOcrPipeline(source_dir=SOURCE, destination_dir=DESTINATION, 
                              parser_backend=PARSER, credentials_config=CREDENTIALS)
   pipeline.process()

Essentially, the pipeline classes let you process collections of documents in a single step, 
as shown in the above examples the pipeline class (``TextOcrPipeline`` in the above example.) 
expects you to define only four parameters - ``source_dir``, ``destination_dir``, ``parser_backend`` and ``credentials`` 
and takes care of the rest.

.. note:: credentials are optional and they need to be provided only if you are using a cloud service 
          such as gcs, s3, google-cloud-vision, aws-textract. Otherwise, you can ignore them and set it to ``None``.
          or if using via config file you can leave the `cloud_credentials.aws` & `cloud_credentials.gcp` field empty.


If you are defining the pipeline config as a yaml file, here is how a sample config file should look like:

.. code-block:: yaml

    storage_config:
        source_dir: "s3://document_bucket/" 
        destination_dir: 'gs://processed_document_bucket/outputs/'

    parser_config:
        parser_backend: "aws-textract"

    cloud_credentials:
        aws: ".credentials/aws-credentials.env"
        gcp: ".credentials/gcp-credentials.json


text extraction with ``ocrpy.io.reader``, ``ocrpy.io.writer`` and ``ocrpy.parsers``
-----------------------------------------------------------------------------------

If you prefer to use ``ocrpy`` from it's lowest level of abstraction, you can do so via the 
``ocrpy.io.reader``, ``ocrpy.io.writer`` and ``ocrpy.parsers`` APIs.

Lets look at an example of doing so. 

.. code-block:: python

    from ocrpy import DocumentReader, StorageWriter, TextParser

    DOC_PATH = 's3://document_bucket/example_document.pdf' # path to an image or pdf file on s3 bucket, gcs bucket or local directory.
    AWS_CREDENTIALS = ".credentials/aws-credentials.env" # path to the aws credentials file.
    GCP_CREDENTIALS = ".credentials/gcp-credentials.json" # path to the gcp credentials file.
    PARSER_BACKEND = 'pytesseract' # or 'google-cloud-vision' or 'pytesseract'

    reader = DocumentReader(file=DOC_PATH, credentials=AWS_CREDENTIALS)
    writer = StorageWriter() 
    text_parser = TextParser(credentials=GCP_CREDENTIALS, backend=PARSER_BACKEND)

    parsed_text = text_parser.parse(reader) # parse the document using the selected parser backend.
    writer.write(parsed_text, "test_output/s3_output/sample-gcp.json") # write the parsed text to a file on s3 bucket, gcs bucket or local directory.

In the above example, we imported ocrpy's ``DocumentReader``, ``StorageWriter`` & ``TextParser`` and 
then used them to parse a document stored on s3 bucket with 'pytesseract' parser backend and wrote the 
parsed text to a file on local directory.

Similarly you can also read document in your local directory, gcs bucket or s3 bucket and parse it 
with any of the parser backends that we currently support and write the parsed text to a file on 
s3 bucket, gcs bucket or local directory as well.

table extraction with ``ocrpy.parsers.table``
---------------------------------------------

Now let's look at how to extract tables from a document using the ``ocrpy.parsers.table`` API.

.. code-block:: python
    
    from ocrpy import DocumentReader, StorageWriter, TableParser

    DOC_PATH = '../documents/example_document_with_table.pdf' # path to an image or pdf file on s3 bucket, gcs bucket or local directory.
    AWS_CREDENTIALS = ".credentials/aws-credentials.env" # path to the aws credentials file.

    reader = DocumentReader(file=DOC_PATH)
    table_parser = TableParser(credentials=AWS_CREDENTIALS)

    parsed_table = table_parser.parse(reader, attempt_csv_conversion=False)

.. note:: ``ocrpy`` currently supports table extraction only with the ``aws-textract`` parser backend. 
            Support for other parser backends will be added soon.


classify documents  with ``ocrpy.experimental.document_classifier``
-------------------------------------------------------------------

In this example let's look at how you can use ``ocrpy`` to classify documents using the 
``ocrpy.experimental.document_classifier`` API.

.. code-block:: python

    from ocrpy import DocumentReader
    from ocrpy.experimental import DocumentClassifier

    DOC_PATH = '../documents/document.img' # path to an image or pdf file on s3 bucket, gcs bucket or local directory.

    reader = DocumentReader(file=DOC_PATH)
    classifier = DocumentClassifier()

    doc_types = classifier.predict(reader)



.. note:: ``ocrpy`` uses HuggingFace's ``transformers`` library in the backend with a pretrained model to perform the classification.
            as such, please make sure you have the ``transformers`` library installed. 

When you run this for the first time, it will download the pretrained model weights and store them in a local directory.
Alternatively you can download or use your own pretrained model weights as well. 
For more info on this see Huggingface `transformers <https://huggingface.co/docs/transformers/index>`_ library documentation.

For more information on the default model and the categories it classifies to, please refer `ocrpy.experimental.document_classifier`.

Parse layout with ``ocrpy.experimental.layout_parser``
---------------------------------------------------

In this example let's look at how you can use ``ocrpy`` to parse layout from a document using the 
``ocrpy.experimental.layout_parser`` API.

.. code-block:: python

    from ocrpy import DocumentReader, TextParser
    from ocrpy.experimental import LayoutParser

    DOC_PATH = '../documents/document.img' # path to an image or pdf file on s3 bucket, gcs bucket or local directory.

    reader = DocumentReader(file=DOC_PATH)
    text_parser = TextParser()
    layout_parser = LayoutParser()

    parsed_layout = layout_parser.parse(reader, text_parser)

.. note:: ``ocrpy`` uses Microsoft's LayoutParser library in the backend to perform the layout parsing.
            as such, please make sure you have the ``layoutparser`` library installed, if not please install it from 
            `LayoutParser <https://github.com/Layout-Parser/layout-parser>`_.

When you run this for the first time, it will download the pretrained model weights and store them in a local directory.
Alternatively you can download or use your own pretrained model weights as well. The model weights can be downloaded from
`LayoutParser Model Catalog <https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html#model-catalog>`_.