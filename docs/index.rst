Python Amazon Creators API
==========================

A Python wrapper for the `Amazon Creators API
<https://webservices.amazon.com/creatorsapi/documentation/>`_, which lets you search
Amazon products, read their details, offers and variations, and list the feeds and
reports of your account.

Install it with:

.. code-block:: bash

   pip install python-amazon-paapi --upgrade

Then create a client with the credentials of the Amazon Associates Creators API portal:

.. code-block:: python

   from amazon_creatorsapi import AmazonCreatorsApi, Country

   api = AmazonCreatorsApi(
       credential_id="your_credential_id",
       credential_secret="your_credential_secret",
       version="2.2",
       tag="your-affiliate-tag",
       country=Country.US,
   )

   items = api.get_items(["B01N5IB20Q"])
   print(items[0].item_info.title.display_value)

The usage guide covers every option of the client, the asynchronous version and the
errors it raises.

Introduction
------------

.. toctree::
   :maxdepth: 2

   ./pages/usage-guide.md

API Reference
-------------

.. toctree::
   :maxdepth: 2

   amazon_creatorsapi
   amazon_creatorsapi.aio
   amazon_creatorsapi.errors
   amazon_creatorsapi.core

.. toctree::
   :maxdepth: 1

   amazon_creatorsapi.models

Migration guides
----------------

Follow the version 7 guide to upgrade code written for ``amazon_creatorsapi`` on version
6. If you are still using the removed ``amazon_paapi`` module, start with the Creators
API guide instead.

.. toctree::
   :maxdepth: 1

   ./pages/migration-guide-7.md
   ./pages/migration-guide-6.md

Changelog
---------

See the `changelog <https://github.com/sergioteula/python-amazon-paapi/blob/master/CHANGELOG.md>`_ for a detailed history of changes.

Support
-------

Ask for help in the `Telegram group <https://t.me/PythonAmazonPAAPI>`_ or open an
`issue <https://github.com/sergioteula/python-amazon-paapi/issues>`_ on GitHub.
