Errors
======

Every error raised by the library inherits from ``AmazonCreatorsApiError``, so a single
``except`` covers them all. The message carries the reason given by Amazon, the fields
that failed validation and the identifier of the request, which is what Amazon support
asks for.

.. automodule:: amazon_creatorsapi.errors
   :members:
   :undoc-members:
   :show-inheritance:
