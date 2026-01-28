Core Utilities
===========================

Core utilities for the Amazon Creators API including country codes and helper functions.

.. autoclass:: amazon_creatorsapi.core.Country
   :show-inheritance:

   **Supported countries:**

   ``AU``, ``BE``, ``BR``, ``CA``, ``DE``, ``ES``, ``FR``, ``IN``, ``IT``,
   ``JP``, ``MX``, ``NL``, ``PL``, ``SA``, ``SE``, ``SG``, ``TR``, ``AE``,
   ``UK``, ``US``

   Example::

       from amazon_creatorsapi.core import Country

       api = AmazonCreatorsApi(..., country=Country.ES)

.. autofunction:: amazon_creatorsapi.core.get_asin
