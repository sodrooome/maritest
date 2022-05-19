=============
HTTP Response
=============

With using maritest, we can also see the HTTP response object from what we have tested before. Basically HTTP responses can be split up into 3 categories, the first is in the form of bytes-like objects, the second is JSON format and the third is multipart. To get these three responses, you need to use the response module from maritest as follows :

.. code-block:: python

    # samples.py
    from maritest.response import Response # import this module

    request = Response(
        method="GET",                          
        url="https://github.com/sodrooome",
        headers={},
    )

.. admonition:: Note
   :class: attention
   
   Incorrect formatting in this ``retriever()`` method arguments will raise the ``NotImplementedError`` message, so consider using the provided format as the following example.

And afterwards you can using the built-in method ``retriever()`` in which there are parameters that used to choose which response we want to get. If you tend to forget to set the format in the parameter, then by default the response will be issued and wrapped in JSON format, so for example to use this method :

HTTP Response Content
---------------------

if you want to get the response content from the server that we are targeting then use the `multipart` format in the argument parameter :

.. code-block:: python

    # same code like above
    >>> request.retriever(format="multipart")

By default, response content using this method will be encoding as ``utf-8`` but you can't change it with another format encoding, since this method is not a method property like ``requests`` do.

Binary Response Content
-----------------------

Another HTTP response that you can access is the response that is bytes-like object in the response body, you can use `bytes` format in the argument parameter :

.. code-block:: python

    >>> request.retriever(format="text")

JSON Response
-------------

And the last HTTP response is the most frequently used is the JSON format, where you can use the built-in JSON decoder that has been provided by Maritest, so for example :

.. code-block:: python

    >>> request.retriever(format="json")

This JSON response using maritest will be slightly different, due the response has been formatted in such a way with the addition of new attributes such as response status code, response time and response headers, all of which aim to simplify the process of debugging information when doing API testing.
If JSON decoding fails it will be caught by exception and will raise ``JSONDecodeError``, other failure when calling format response will be caught by basic ``Exception`` with error message.

Formatted Raw Response Content
------------------------------

In addition to the three HTTP responses, **Maritest** also provides a custom method to return a formatted raw HTTP response, you can use it looks like this :

.. code-block:: python

    # samples.py
    from maritest.response import Response

    request = Response(
        method="GET",                          
        url="https://jsonplaceholder.typicode.com/posts/1",
        headers={},
    )

    # call this method to returned raw HTTP response
    response = request.http_response()

    # the output will be like this
    ------------------Maritest Request------------------
    GET https://jsonplaceholder.typicode.com/posts/1
    User-Agent : python-requests/2.25.1
    Accept-Encoding : gzip, deflate
    Accept : */*
    Connection : keep-alive
    Content-Length : 2
    Content-Type : application/json

    b'{}'
    ------------------Maritest Response-----------------
    200 https://jsonplaceholder.typicode.com/posts/1
    Date : Tue, 12 Apr 2022 22:17:04 GMT
    Content-Type : application/json; charset=utf-8
    Transfer-Encoding : chunked
    Connection : keep-alive
    X-Powered-By : Express
    X-Ratelimit-Limit : 1000
    X-Ratelimit-Remaining : 999
    X-Ratelimit-Reset : 1648136288
    Vary : Origin, Accept-Encoding
    Access-Control-Allow-Credentials : true
    Cache-Control : max-age=43200
    Pragma : no-cache
    Expires : -1
    X-Content-Type-Options : nosniff
    Etag : W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
    Via : 1.1 vegur
    CF-Cache-Status : HIT
    Age : 13447
    Expect-CT : max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
    Report-To : {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v3?s=5chv0JQeD7j1VAdCTLfaHItWIxB%2BSPmeEv1wT0%2FfdCoc3mVCmD8o7MBxwGR7ca8UMOG5FZeIrDRvIhbcgRGZyyo4KVxTOuVQ37%2FAZyQjrhKYL%2Bskijw0rwpONvTMDtOi7sCb%2B6jm4mTvDbpYJPTM"}],"group":"cf-nel","max_age":604800}
    NEL : {"success_fraction":0,"report_to":"cf-nel","max_age":604800}
    Server : cloudflare
    CF-RAY : 6faf547cfe6301c4-SIN
    Content-Encoding : gzip
    alt-svc : h3=":443"; ma=86400, h3-29=":443"; ma=86400

History Redirection
-------------------

Besides that, if you want to see how many times your HTTP target does redirection, you can use another method that called from the response module, to do this ensure that you also enabling the ``allow_redirects`` argument in parameter. Consider to use this method if the HTTP target you are targeting gets a status code like ``301`` or move permanently, for example :

.. code-block:: python

    >>> from maritest.response import Response
    >>> request = Response(method="GET", url="http://github.com/", allow_redirects=True)
    >>> request.history_response()

    # the output will be like this
    URL redirects : http://github.com/
    Count history : 1 [None]
