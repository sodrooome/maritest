==============
Authentication
==============

**Maritest** has also provided several methods to use user authentication when making requests to the HTTP target. Basically, this framework support common user authentication like

- `BasicAuth`
- `DigestAuth`
- `BearerAuthToken`
- `BasicAuthToken`
- `APIKeyAuth`

To use this, we need to import another module and define the `auth` argument as follows :

.. code-block:: python

    # samples.py
    from maritest.assert import Assert
    from maritest.custom_auth import BasicAuth # NEW: import this module

    request = Assert(
        method="POST",                          
        url="https://github.com/sodrooome",
        headers={"content-type": "application/json"},
        auth=BasicAuth(...) # NEW: call auth argument keyword
    )

    # do HTTP assert like previous example
    request.assert_is_ok(message="Request must be loggedin")


Basic authentication
--------------------

Usage of `BasicAuth`, this method used to perform basic authentication by simply using a username or password to the intended HTTP request. For example :

.. code-block:: python
    
    >>> request = Assert(..., auth=BasicAuth(username="sodrooome", password="hahaha"))

Digest authentication
---------------------

Usage of `DigestAuth`, this method has the same function like basic authentication but has a better security aspect. For example :

.. code-block:: python

    >>> request = Assert(..., auth=DigestAuth(username="sodrooome", password="hahaha"))

Bearer auth token
-----------------

Usage of `BearerAuthToken`, this method only accept authentication with bearer token provided. For example :

.. code-block:: python

    >>> request = Assert(..., auth=BearerAuthToken(token="xmoasduuDK'asdj1"))


Basic auth token
----------------

Usage of `BasicAuthToken`, this method only accept authentication with basic token provided. For example :

.. code-block:: python

    >>> request = Assert(..., auth=BasicAuthToken(token="basic-token"))

Api key authentication
----------------------

Usage of `APIKeyAuth`, this method inspired by one type of authentication in postman. Apparently, this is a custom authentication that is not provided by the requests package. Using this method, you need to pass a key value into the related argument and also add a value for the `add_to` argument which will be sent to the corresponding headers. There are 2 choices for `add_to` argument, first choice is appending request to `headers` and second choice is append request to `query_params` in url, all 3 arguments are required, for example :

.. code-block:: python

    >>> request = Assert(..., auth=APIKeyAuth(key="your-key", value="your-value", add_to="query_params"))
