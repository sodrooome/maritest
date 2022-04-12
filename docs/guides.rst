======
Guides
======

General Usage
-------------

There are several ways for using this framework, the first one is when you send the request to the HTTP target, and this can be done by calling the `Assert` or `Http` method. Basic usage would be like this :

.. code-block:: python

    >>> from maritest.assertion import Assert
    >>> from maritest.assertion import Http # or, you can use this method

    >>> request = Assert(method="GET", url="http://your-url", headers={})
    >>> request.assert_is_ok(message=None)


**important keynotes** : argument for `method`, `url` and `headers` are required, so you'll expected to full fill all of them. If you feel that you don't need `headers` argument, you can fill it with empty `dict` .

Other keynote is, the different usage when using `Assert` and `Http` method are when using the `Http` method, **you will not be able** to do assertion tests for the target because that method is an abstract base class for the `Assert` class. Other than that, the use of parameters and functions will remain the same

There are several arguments / parameters that you can also pass it when making an HTTP request, and the mechanism itself is similar to when you use the requests package. those arguments consisted of :

Enable logger
-------------

Enable logger argument for stream handler the log request and response while doing HTTP request. This logger is used for debugging if an error occurs when making an assertion
    
.. code-block:: python
    
    >>> request = Assert(method="GET", url="http://your-url", logger=True)

    # the output will like this
    08-02-2022 12:14:26 : Maritest Logger : __init__ : [INFO] HTTP Request POST => https://httpbin.org/post
    08-02-2022 12:14:26 : Maritest Logger : __init__ : [DEBUG] HTTP Request {'some': 'value'} => https://httpbin.org/post
    08-02-2022 12:14:27 : Maritest Logger : __init__ : [INFO] HTTP Response 200
    
    
**important keynote** : if you tend to disabled the logger argument, you will receive a response log file in your local, the file name is “maritest.log”

Allow redirections for HTTP
---------------------------

Enable allow_redirects parameter. This will request other HTTP target if the existing or previous one wasn't respond yet.

.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", allow_redirects=True)


Perform retry mechanism
-----------------------

Enable retry parameter to retry and send HTTP request again. Particularly, i do not recommend use this method due it will slowing down the performance process. For example :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", retry=True)


Using timeout to delay request
------------------------------

Using `timeout` mechanism instead `retry`. By default the `timeout` parameter duration will be set to 120 seconds (or 2 minutes), but you can change it according to your needs. For example :
    
.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", timeout=None) # 120 secs
    >>> request = Assert(method="GET", url="http://your-url", timeout=60) # 1 minute
    
Event hooks when error raises
-----------------------------

Enable `event_hooks` when requested HTTP target. This parameter only trigger if the HTTP target gives an error code like 404, if the event hook is not used, then on the client side it will only display the built-in exception that is already provided in Maritest. For example :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://404-not-found", event_hooks=True)
    
    # when enable event_hooks, the output will be like this
    requests.exceptions.HTTPError: 404 Client Error: NOT FOUND for url: http://404-not-found

Suppressing warning message
---------------------------

Disable suppressed warning message about SSL certification. For this one particularly is not advise to do it (same as like requests did), it's strongly advise to add certification path, for example :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://404-not-found", supress_warning=True)

    # you'll receive the information about deprecation warning instead
    UserWarning: parameter `suppressed_warning` will be deprecated and no longer use in the next release consider to add certification path instead or always enable the SSL verification issue
        warnings.warn(
    [WARNING] SSL verification status is disabled

Proxy request to HTTP target
----------------------------

Using proxy to request HTTP target. You can configure 1 instance of proxy request with proxy arguments. Whenever you set or store proxy values in dict object, you need to set the HTTP scheme also (HTTP/HTTPS) otherwise the proxy values that you configured will be act as HTTP scheme so it won't do redirection to actual target. For example :

.. code-block:: python

    >>> proxy = {"https": "https://github.com"}
    >>> request = Assert(method="GET", url="http://github.com/", proxy=proxy)
