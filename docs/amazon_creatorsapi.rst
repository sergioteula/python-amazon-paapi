API module
==========

This is the main class that provides authentication and methods for accessing the Amazon
Creators API. Instance it with your credentials and configuration, and reuse it: it keeps
a pool of connections open, which ``close`` and the context manager release.

.. autoclass:: amazon_creatorsapi.api.AmazonCreatorsApi
   :members:
   :undoc-members:
   :show-inheritance:
