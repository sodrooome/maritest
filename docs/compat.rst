=======================
Interface Compatibility
=======================

Maritest is built on top of the ``requests`` library and basically the overall functionality will be exactly same like what requests do,
however there will be some differences in design when using this library (which is confusing if you are familiar with ``requests``). Here are the differences :

Calling HTTP client instances
-----------------------------

What ``requests`` did when call the `Session` is :

.. code-block:: python

    >>> requests.Session()

Or also can call based on HTTP verb method directly like this :

.. code-block:: python

    >>> requests.get("https://github.com")

While using Maritest, calling the HTTP client can only be done using the Http class instance (and cannot use the HTTP verb method)

.. code-block:: python

    >>> Http("GET", "https://github.com")

HTTP response object
--------------------

Using ``requests``, if we want to access the response object in the form of ``JSON``, ``content`` or ``text`` we can use the property according to the attribute name such as :

.. code-block:: python

    >>> resp = requests.get(...)
    >>> resp.json()
    >>> resp.text

Using this library calling is quite the same using property also but with a slight difference

.. code-block:: python

    >>> resp = Http(...)
    >>> resp.get_json
    >>> resp.get_text

Headers parameter must be set
-----------------------------

Another difference is that in this library we need and **must** to set headers or custom headers when making a request to the target,
if we don't set the headers parameter in the request body it will raise an ``AssertionError`` and this is of course very different from ``requests``
because the use of the headers parameter is optional and can be set as ``None`` object. If you feel that no need to setup
headers parameter then you can set as empty dict without key and value.

Set headers when using ``requests`` library

.. code-block:: python

    >>> resp = requests.get(..., headers=None) # able to set as None type
    ... 200

Set headers as ``None`` type when using Maritest

.. code-block:: python

    >>> resp = Http(... headers=None) # not able to set as None type
    ...     assert isinstance(headers, dict), "headers must be dict object"
    ... AssertionError: headers must be dict object

Set headers as empty dictionary

.. code-block:: python

    >>> resp = Http(... headers={}) # set as empty dict instead
    ... 200