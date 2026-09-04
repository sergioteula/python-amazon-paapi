Async API module
================

The async version of the API provides the same methods, parameters and errors as the
synchronous one, but uses ``async/await`` for non-blocking operations. It requires
``httpx``, which comes with the ``async`` extra.

Installation
------------

.. code-block:: bash

   pip install python-amazon-paapi[async] --upgrade

Usage
-----

Used as an async context manager, the client keeps a single connection open for every
request made inside it. Outside of one, each request opens and closes its own connection,
so there is nothing to release and the client has no ``close`` method.

.. code-block:: python

   from amazon_creatorsapi import Country
   from amazon_creatorsapi.aio import AsyncAmazonCreatorsApi

   async with AsyncAmazonCreatorsApi(
       credential_id="your_credential_id",
       credential_secret="your_credential_secret",
       version="2.2",
       tag="your-affiliate-tag",
       country=Country.US,
   ) as api:
       items = await api.get_items(["B01N5IB20Q"])

API Reference
-------------

.. autoclass:: amazon_creatorsapi.aio.api.AsyncAmazonCreatorsApi
   :members:
   :undoc-members:
   :show-inheritance:
