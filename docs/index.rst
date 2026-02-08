.. python-amazon-paapi documentation master file, created by
   sphinx-quickstart on Mon Nov 22 18:33:43 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Amazon Creators API's documentation!
======================================================

A simple Python wrapper for the Amazon Creators API.
This module allows interacting with Amazon using the official APIs in an easier way.

.. note::

   The ``amazon_paapi`` module is deprecated. New projects should use the ``amazon_creatorsapi``
   module instead. See the :doc:`./pages/migration-guide-6` for migration instructions.

Introduction
---------------

.. toctree::
   :maxdepth: 1

   ./pages/usage-guide.md

API Reference
----------------------

.. toctree::

   amazon_creatorsapi
   amazon_creatorsapi.aio
   amazon_creatorsapi.errors

.. toctree::
   :maxdepth: 2

   amazon_creatorsapi.core

.. toctree::
   :maxdepth: 1

   amazon_creatorsapi.models

Migration guide
---------------

If you are still using version 5.x or lower, it is recommended upgrading to the latest version.

.. toctree::
   :maxdepth: 1

   ./pages/migration-guide-6.md

Changelog
---------

See the `changelog <https://github.com/sergioteula/python-amazon-paapi/blob/master/CHANGELOG.md>`_ for a detailed history of changes.
