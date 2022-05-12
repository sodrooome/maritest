===============
Assertion Usage
===============

Here are a collection of useful built-in assertion methods that have been provided by Maritest. The use of this assertion needs to be initiated from the Assert class instead.
Basically, if the entire assertion or testing process against the HTTP target fails using the method below, it will raise an ``AssertionError``.

.. admonition:: Important Keynote
   :class: important

   The built-in method for all these assertions has 1 required argument that needs to be filled, it call the argument for the ``message`` where this argument takes and will send the a brief of user message expectation after execute request.

Assert request is ok
--------------------

Test to check whether the HTTP request is ok or not

.. code-block:: python

    from maritest.assertion import Assert

    response = Assert(
        method="GET",
        url="https://jsonplaceholder.typicode.com/posts/1",
        headers={} # set to empty dict if not needed
    )

    response.assert_is_ok(message="request should be success")

Assert request is failed
------------------------

Test to check whether the HTTP request is failed at the first attempt or not

.. code-block:: python
    
    response.assert_is_failed(message="request should be failed")

Assert request has headers
--------------------------

Test to check whether the HTTP request has HTTP headers or not, will check all possibilities of HTTP headers

.. code-block:: python

    response.assert_is_headers(message="request has headers")

Assert request has content-type
-------------------------------

Test to check whether the HTTP request has content-type or not

.. code-block:: python

    response.assert_is_content_type(message="request has content-type")

Assert request content-type equal to expected result
----------------------------------------------------

Test if the HTTP request has content-type is equal to expected argument that we set

.. code-block:: python

    response.assert_content_type_to_equal(
        message="content-type was equal", 
        value="application/json; charset=utf-8"
    )

Assert response status code is in range 2xx
-------------------------------------------

Test if the HTTP response status code within range 2xx

.. code-block:: python

    response.assert_is_2xx_status(message="status code in 2xx")

Assert response status code is in range 3xx
-------------------------------------------

Test if the HTTP response status code within range 3xx

.. code-block:: python

    response.assert_is_3xx_status(message="status code in 3xx")


Assert response status code is in range 4xx
-------------------------------------------

Test if the HTTP response status code within range 4xx

.. code-block:: python

    response.assert_is_4xx_status(message="status code in 4xx")

Assert response status code is in range 5xx
-------------------------------------------

Test if the HTTP response status code within range 5xx

.. code-block:: python

    response.assert_is_5xx_status(message="status code in 5xx")

Assert request has content response
-----------------------------------

Test if the HTTP response has content body

.. code-block:: python

    response.assert_has_content(message="response has content body")

Assert request has JSON response
--------------------------------

Test if the HTTP response has JSON body

.. code-block:: python

    response.assert_has_json(message="response has json response")

Assert request has multipart response
-------------------------------------

Test if the HTTP response has multipart/text response

.. code-block:: python

    response.assert_has_text(message="response has text")

Assert response status code in expected range
---------------------------------------------

Test whether HTTP response status code within expected range that we set before

.. code-block:: python

    response.assert_status_code_in(
        status_code=[200, 201], 
        message="status code should be in that range"
    )

Assert response status code not in expected range
-------------------------------------------------

Test whether HTTP response status code not in expected range that we set before

.. code-block:: python

    response.assert_status_code_not_in(
        status_code=[400, 404],
        message="status code should be not in that range"
    )

Assert validate JSON response equal to expected result
------------------------------------------------------

Validate whether JSON response body is equal to expected result that we set before

.. code-block:: python

    expected_result = {"key": "value"}

    response.assert_json_to_equal(
        obj=expected_result,
        message="JSON response must be equal"
    )

Assert validate text response equal to expected result
------------------------------------------------------

Validate whether text response body is equal to expected result that we set before

.. code-block:: python

    expected_result =  b'eum\\naccusamus ratione error aut"\n}'

    response.assert_text_to_equal(
        obj=expected_result,
        message="text response must be equal"
    )

Assert that response time less with duration
--------------------------------------------

Test whether the HTTP response time is less than 200 seconds or maximum duration that already defined previously

.. code-block:: python

    response.assert_response_time_less(message="response time shouldn't be exceed the limit")

Assert response time
--------------------

Test whether the HTTP response time is less than duration of time that we set. Argument duration is integer type

.. code-block:: python

    response.assert_response_time(duration=90, message="response time shouldn't be exceed the duration")

Assert request has content-length
---------------------------------

Test whether the HTTP request has set the content-length

.. code-block:: python

    response.assert_content_length(message="response has content-length")

Assert that request expected to be fail
---------------------------------------

Test if the HTTP request was expected to be failed instead of getting success

.. code-block:: python

    response.assert_expected_to_fail(message="this request must be failed")

Assert request TLS is secure
----------------------------

Test whether the TLS connection that has been made is secure, insecure or not valid scheme

.. code-block:: python

    response.assert_tls_secure(message=None) # you can set as None-type of object
