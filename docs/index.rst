.. maritest documentation master file, created by
   sphinx-quickstart on Wed Apr 13 03:50:10 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Maritest Docs
=============

.. image:: https://github.com/sodrooome/maritest/actions/workflows/test.yml/badge.svg
   :target: https://github.com/sodrooome/maritest/actions/workflows/test.yml/badge.svg
   :alt: Pipeline Passing

.. image:: https://img.shields.io/pypi/pyversions/maritest
   :target: https://img.shields.io/pypi/pyversions/maritest
   :alt: Python version

.. image:: https://codecov.io/gh/sodrooome/maritest/branch/master/graph/badge.svg?token=H3K1JNZBW2
   :target: https://codecov.io/gh/sodrooome/maritest/branch/master/graph/badge.svg?token=H3K1JNZBW2
   :alt: Code coverage

.. image:: https://img.shields.io/pypi/status/maritest
   :target: https://img.shields.io/pypi/status/maritest
   :alt: Python status

Summary
-------

**Maritest** is an API testing framework that the purpose's solely to simplifying assertion when doing testing in API layer, it's an easy and convenient way to go iterative testing while keep up the fast-paced development and be able to maintain all testing modules / scenarios without breaking change

Features
--------

- Extending usage when doing HTTP request
- Easy-to-use thanks to `requests` library
- Built-in assertion to make easier when doing API testing

Quick Usage
-----------

*Maritest well-tested on Python version 3.7 and above, you may still be able to use it with Python 3.7 below but it's expected there's backward compatibility that will happen*

The installation can be done with :

.. code-block:: bash

   pip install maritest

After you're done with installation, you can try to use this basic feature from **Maritest** for example :

.. code-block:: python

      # samples.py
      from maritest.assertion import Assert

      request = Assert(
         method="GET",                          
         url="https://github.com/sodrooome",
         headers={},
      )

      # pick it up several method what kind of assertion that you wanted
      # 1. Assert status code is 2xx
      # 2. Assert request is failed or not
      # 3. Assert content-type of HTTP
      # 4. Assert response time when request HTTP
      request.assert_status_is_2xx(message=None)
      request.assert_is_failed(message="Shouldn't be failed")
      request.assert_is_content_type(message=None)
      request.assert_response_time(duration=300)

Afterwards, wrap up that configuration and just run that file and it will automatically, the assertion testing process will execute without us needs to define the actual result or also set the expected result. If any of the assertion methods above it's fail, it will raise an error message.

For more detailed information of using **Maritest** please refer to the general usage.

.. toctree::
   :hidden:
    
   guides
   assertion
   authentication
   response
   changelog
   upcoming
   references
