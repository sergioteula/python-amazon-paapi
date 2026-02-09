Async API module
========================

The async version of the API provides the same functionality as the synchronous API, but uses
``async/await`` for non-blocking operations. Requires ``httpx`` for HTTP requests.

Installation
------------

Install with async support:

.. code-block:: bash

   pip install python-amazon-paapi[async] --upgrade

API Reference
-------------

.. autoclass:: amazon_creatorsapi.aio.api.AsyncAmazonCreatorsApi
   :members:
   :undoc-members:
   :show-inheritance:
