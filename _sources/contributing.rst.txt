Contributing to ocrpy
=====================

All you need to know to contribute to ocrpy, effectively. 

Codebase structure
-------------------

- Ocrpy codebase on github: `Ocrpy Codebase <https://github.com/maxent-ai/ocrpy/tree/main/ocrpy>`_
- Python unit tests: `Tests <https://github.com/maxent-ai/ocrpy/tree/main/tests>`_
- Ocrpy documentation: `Docs <https://github.com/maxent-ai/ocrpy/tree/main/docs>`_
- Ocrpy tutorials: `Notebooks <https://github.com/maxent-ai/ocrpy/>`_


Continuous Integration
----------------------

This project uses the following integrations to ensure proper codebase maintenance:

- Run jobs for package build and coverage: `Github Worklow <https://help.github.com/en/actions/configuring-and-managing-workflows/configuring-a-workflow>`_
- Reports back coverage results: `Codecov <https://codecov.io/>`_
- As a contributor, please ensure that you write unit tests for your code and run coverage tests for your code before submitting a pull request.

Feedback
--------

Feature requests & bug report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Whether you encountered a problem, or you have a feature suggestion, your input has value and can be used by contributors to reference it in their developments. For this purpose, we advise you to use Github issues.Please submit them at `Github Issues <https://github.com/maxent-ai/ocrpy/issues>`_
- First, check whether the topic wasn't already covered in an open / closed issue. If not, feel free to open a new one! When doing so, use issue templates whenever possible and provide enough information for other contributors to jump in.

Questions
^^^^^^^^^^

If you are wondering how to do something with ocrpy, or a more general question, you should consider checking out Github discussions at `Github Discussions <https://github.com/maxent-ai/ocrpy/discussions>`_

Developing ocrpy
----------------

Developer mode installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install all additional dependencies with the following command:

.. code-block:: console

    pip install -e .[dev]

Commits
------

- **Code**: ensure to provide docstrings to your Python code. In doing so, please follow `Google-style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_ so it can ease the process of documentation later.
- **Commit message**: please follow `Udacity guide <http://udacity.github.io/git-styleguide/>`_ 


Unit tests
---------

In order to run the same unit tests as the CI workflows, you can run unittests locally:

.. code-block:: console

    make test


Code Quality
------------

To run all quality checks together

.. code-block:: console
    
    make quality


Linting
^^^^^^^

To ensure that your incoming PR complies with the lint settings, you need to install `black <https://black.readthedocs.io/en/stable/>`_ and run the following command from the repository's root folder:

.. code-block:: console

    black ./

Import format
^^^^^^^^^^^

In order to ensure there is a common import order convention, run `isort <https://github.com/PyCQA/isort>`_ as follows:

.. code-block:: console

    isort **/*.py

This will reorder the imports of your local files.

Type Annotations
^^^^^^^^^^^^^^^

Additionally, to catch type-related issues and have a cleaner codebase, annotation typing are expected. After installing `mypy <https://github.com/python/mypy>`_, you can run the verifications as follows:

.. code-block:: console

    mypy --config-file mypy.ini ocrpy/

The `mypy.ini` file will be read to check your typing.


Docstring format
^^^^^^^^^^^^^^^^

Please follow Google style for docstrings which can be found over here: `Google-style <https://google.github.io/styleguide/pyguide.html>`_

Modifying the documentation
----------------------------

In order to check locally your modifications to the documentation:

.. code-block:: console

    cd docs
    make clean html 
```
You can now open your local version of the documentation located at `docs/_build/index.html` in your browser.


Let's connect
----------------

Should you wish to connect somewhere else than on GitHub, feel free to reach out to us at info@maxentlabs.com




