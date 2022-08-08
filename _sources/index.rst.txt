.. module:: ocrpy 

OcrPy Documentation
===================

The Core objective of OcrPy is to let users OCR, Archive, Index and Search any documents with ease, 
with a simple and intuitive interface and a powerful Pipeline API. 

`ocrpy`  achieves this by wrapping around various OCR engines like `Tesseract OCR <https://tesseract-ocr.github.io/>`_, `Aws Textract <https://aws.amazon.com/textract/>`_, 
`Google Cloud Vision <https://cloud.google.com/vision/docs/ocr>`_ and `Azure Computer Vision <https://azure.microsoft.com/en-in/services/cognitive-services/computer-vision/#features>`_.
It unifies the multitude of interfaces provided by a wide range of cloud tools & other open-source libraries 
and provides a simple, easy-to-use interface for the user.

.. image:: _static/ocrpy-overview-plain.png
   :align: center
   :alt: ocrpy overview
   :height: 400px

Getting Started
===============

``ocrpy`` is a Python-only package `hosted on PyPI <https://pypi.org/project/ocrpy/>`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_

.. code-block:: console

   $ python -m pip install ocrpy



Day-to-Day Usage
================

Ocrpy Provides various levels of abstraction for the user to perform OCR on various types of documents. 
The recommended and the best way to use Ocrpy is to use it through it's `pipelines` API as shown below.

The Pipeline API can be invoked in two ways. The first method is to define the config for running the 
pipeline as a yaml file and and then run the pipeline by loading it as follows: 

.. code-block:: python

   from ocrpy import TextOcrPipeline

   ocr_pipeline = TextOcrPipeline.from_config("ocrpy_config.yaml")
   ocr_pipeline.process()

alternatively you can also run a pipeline by directly instantiating the pipeline class as follows:

.. code-block:: python

   from ocrpy import TextOcrPipeline

   pipeline = TextOcrPipeline(source_dir='s3://document_bucket/', 
                              destination_dir="gs://processed_document_bucket/outputs/", 
                              parser_backend='aws-textract', 
                              credentials_config={"AWS": "path/to/aws-credentials.env/file", 
                                           "GCP": "path/to/gcp-credentials.json/file"})
   pipeline.process()

.. note :: For a more detailed explanation of the ``pipelines`` API, please refer to the `ocrpy.pipelines` section of the documentation 
           & please check out the examples and tutorials for a more in-depth understanding of how to leverage ocrpy.

Full Table of Contents
======================

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   overview
   examples
   tutorials

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api-reference
   system-design

.. toctree::
   :maxdepth: 1
   :caption: Contributing to ocrpy

   contributing
   code-of-conduct
   license-and-credits


.. note :: For a full index of all the functionalities, see the :ref:`genindex`
