======
Guides
======

General Usage
-------------

There are several ways for using this library, the first one is when you send the request to the HTTP target, and this can be done by calling the ``Assert`` or ``Http`` method. Basic usage would be like this :

.. code-block:: python

    >>> from maritest.assertion import Assert
    >>> from maritest.assertion import Http # or, you can use this method

    >>> request = Assert(method="GET", url="http://your-url", headers={})
    >>> request.assert_is_ok(message=None)

.. admonition:: Keynote
   :class: important
   
   argument for ``method``, ``url`` and ``headers`` are required, so you'll expected to full fill all of them. If you feel that you don't need ``headers`` argument, you can fill it with empty ``dict``.

Other keynote is, the different usage when using ``Assert`` and ``Http`` method are when using the ``Http`` method, you will not be able to do assertion tests for the target because that method is an abstract base class for the ``Assert`` class. Other than that, the use of parameters and functions will remain the same.
For example if you mistakenly use assertion with ``Http`` class, then you will get ``NotImplementedError`` message like this :

.. code-block:: bash

    line 407, in assert_is_2xx_status
        raise NotImplementedError
    NotImplementedError

Or you can also define the ``Assert`` with context manager by using ``with`` statement. With this, the request process will close its connection after the process is complete so it's a pretty convenient way to expressing try-catch exception in simplistic code

.. code-block:: python

    >>> from maritest.assertion import Assert
    >>> request = Assert(method="GET", url="http://target-url", headers={})
    >>> with request as resp:
    ...     resp.assert_is_ok(message="Response must be success")
    ...     resp.assert_is_failed(message="Response must not failed")

There are several arguments or parameters that you can also pass it when making an HTTP request, and the mechanism itself is similar to when you use the ``requests`` package. those arguments consisted of :

Enable logger
-------------

Enable ``logger`` argument for stream handler the log request and response while doing HTTP request. This logger is used for debugging if an error occurs when making an assertion
    
.. code-block:: python
    
    >>> request = Assert(method="GET", url="http://your-url", logger=True)

    # the output will like this
    08-02-2022 12:14:26 : Maritest Logger : __init__ : [INFO] HTTP Request POST => https://httpbin.org/post
    08-02-2022 12:14:26 : Maritest Logger : __init__ : [DEBUG] HTTP Request {'some': 'value'} => https://httpbin.org/post
    08-02-2022 12:14:27 : Maritest Logger : __init__ : [INFO] HTTP Response 200
    
    
.. admonition:: Keynote
   :class: important
   
   if you tend to disabled the logger parameter, you will receive a response log file in your local, the file name is “maritest.log”

Allow redirections for HTTP
---------------------------

Enable ``allow_redirects`` parameter. This will request other HTTP target if the existing or previous one wasn't respond yet.

.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", allow_redirects=True)


Setup custom HTTP headers
-------------------------

Same as like package ``requests`` did, you can also setup and configure custom HTTP Headers by passing it into ``headers`` argument in parameter as follow :

.. code-block:: python

    >>> headers = {"Content-Type": "application/json; charset=utf-8"}
    >>> request = Assert(method="GET", url="https://your-url", headers=headers)


Perform retry mechanism
-----------------------

Enable ``retry`` parameter to retry and send HTTP request again. Particularly, i do not recommend use this method due it will slowing down the performance process. For example :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", retry=True)

You eventually can see whether the retry function is being process or not by enabling the logger parameter same as like on the previous example. If you tend to disable this retry argument, the log stream handler will informed you like :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", retry=False, logger=True)

    # information from logger
    19-12-2021 12:12:30 : Maritest Logger : __init__ : [INFO] HTTP retry method might be turned it off


Using timeout to delay request
------------------------------

Using ``timeout`` mechanism instead ``retry``. By default the ``timeout`` parameter duration will be set to 120 seconds (or 2 minutes), but you can change it according to your needs. For example :
    
.. code-block:: python

    >>> request = Assert(method="GET", url="http://your-url", timeout=None) # 120 secs
    >>> request = Assert(method="GET", url="http://your-url", timeout=60) # 1 minute
    
Event hooks when error raises
-----------------------------

Enable ``event_hooks`` when requested HTTP target. This parameter only trigger if the HTTP target gives an error code like 404, if the event hook is not used, then on the client side it will only display the built-in exception that is already provided in Maritest. For example :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://404-not-found", event_hooks=True)
    
    # when enable event_hooks, the output will be like this
    requests.exceptions.HTTPError: 404 Client Error: NOT FOUND for url: http://404-not-found

    # when disable event_hooks, the output by default using exceptions
    line 61, in assert_is_2xx_status
        raise AssertionError(message)
    AssertionError: The status not 2xx

Suppressing warning message
---------------------------

Disable suppressed warning message about SSL certification. For this one particularly is not advise to do it (same as like requests did), it's strongly advise to add certification path, for example :

.. code-block:: python

    >>> request = Assert(method="GET", url="http://404-not-found", supress_warning=True)

    # you'll receive the information about deprecation warning instead
    UserWarning: parameter `suppressed_warning` will be deprecated and no longer use in the next release consider to add certification path instead or always enable the SSL verification issue
        warnings.warn(
    [WARNING] SSL verification status is disabled

User authentication
-------------------

you can also use user authentication to target HTTP if needed, for that call ``auth`` argument into it and import module ``custom_auth`` to use the multiple types of HTTP authentication provided as follow :

.. code-block:: python

    # examples.py
    from maritest.assert import Assert
    from maritest.custom_auth import BasicAuth

    basic_auth = BasicAuth(username="your-name", password="your-password")
    request = Assert(method="POST", url="your-url-target", auth=basic_auth)

To learn about and use different HTTP authentication please read the page about `Authentication <https://maritest.readthedocs.io/en/latest/authentication.html>`_

Proxy request to HTTP target
----------------------------

Using proxy to request HTTP target. You can configure 1 instance of proxy request with proxy arguments. Whenever you set or store proxy values in dict object, you need to set the HTTP scheme also (HTTP/HTTPS) otherwise the proxy values that you configured will be act as HTTP scheme so it won't do redirection to actual target. For example :

.. code-block:: python

    >>> proxy = {"https": "https://github.com"}
    >>> request = Assert(method="GET", url="http://github.com/", proxy=proxy)

Send request with data argument
-------------------------------

Send request to the HTTP target with data as body information in the form of bytes, tuple or dictionary. For example :

.. code-block:: python

    >>> data_payload = {"key": "value"}
    >>> request = Assert(method="POST", url="https://httpbin.org/post", headers={}, data=data_payload)

there are some cases where you need to process the encoding of the JSON to a string object when using the data argument, for that you need to do dumping first before make request, such as :

.. code-block:: python

    >>> data_payload = {"key": "value"}
    >>> json_dump = json.dumps(data_payload)
    >>> request = Assert(method="POST", url="https://httpbin.org/post", headers={}, data=json_dump)

Send request with multipart-encoded files
-----------------------------------------

Send request to the HTTP target with ``files`` argument in the form of bytes, multiple file-like object or dictionary. For example :

.. code-block:: python

    # samples.py
    request = Http(
        method="POST",
        url="https://httpbin.org/post",
        headers={},
        files={"file": ("report.csv", "some,data,to,send\nanother,row,to,send\n")},
        timeout=True,
    )

    request.assert_is_ok(message="request was OK!")

Send request with encoded dict object
-------------------------------------

To achieve this, you can using ``json`` argument without need to encoded anymore. For example :

.. code-block:: python

    json_payload = {"key": "value"}

    request = Http(
        method="POST",
        url="https://httpbin.org/post",
        headers={},
        json=json_payload,
        timeout=True,
    )

    request.assert_has_json(message="Response should be has JSON!")

Using query parameters
----------------------

You can also use a parameterized query to the given URL, such as :

.. code-block:: python

    payload_params = {"key1": "value1", "key2": "value2"}
    request = Http(
        method="GET",
        url="https://httpbin.org/get",
        headers={},
        timeout=False,
        params=payload_params,
    )

    # call the url object to
    # returned full-path URL
    print(request.response.url)
    
    # the result
    >>> "https://httpbin.org/get?key1=value1&key2=value2"

Streaming requests to HTTP target
---------------------------------

You can also possibly to streaming media / files over HTTP target by enabling ``stream`` argument and call the ``streaming_requests()`` method. For example :

.. code-block:: python

    request = Http(
        method="GET",
        url="https://httpbin.org/stream/20",
        headers={},
        timeout=10,
        logger=True,
        stream=True # enable stream argument
    )

    # call this method
    # block_size -> represent numbers of chunk size
    # format -> represent type extension of file format
    request.streaming_requests(block_size=1024, format="txt")

    # the result
    >>> 2.81kiB [00:00, 11.1kiB/s]11-05-2022 10:45:27 : client.py : streaming_requests : [INFO] Finished streaming requests

There are several argument constructors that needed when calling the ``streaming_requests()`` method. Mandatory arguments are ``block_size`` and ``format``, while
other arguments are optional such as ``decode`` and ``rate_limit``. If you streaming APIs to a large media size, then you can see the progress bar on your command line as below, this can happen thanks to ``tqdm`` package

.. code-block:: bash

    11-05-2022 10:40:17 : client.py : streaming_requests : [INFO] Streaming requests over APIs ...
    100%|██████████████████████████████████████████████████████████████████████▉| 10.5M/10.5M [00:17<00:00, 717kiB/s]11-05-2022 10:40:38 : client.py : streaming_requests : [INFO] Finished streaming requests
    