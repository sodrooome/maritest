================
Further Examples 
================

Some collection of further examples related to using **Maritest**

Generate tests report
---------------------

for this example, you need to install **HtmlTestRunner** and you can see the following example (here we are using unittest for testing as usual)

.. code-block:: python

    # test_suites.py
    import HtmlTestRunner
    import unittest
    from maritest.assert import Assert

    class TestServices(unittest.TestCase):
        def setUp(self) -> None:
            self.request = Assert(
                method="GET",
                url="https://jsonplaceholder.typicode.com/posts",
                headers={"some_key": "some_value"},
                proxies=None,
                logger=True,
                supress_warning=False,
                verify=True
            )

        def test_assert_is_ok(self):
            self.request.assert_is_ok(message="request was success")
            self.request.assert_is_2xx_status(message="status is 2xx")

        def test_assert_status_code(self):
            self.request.assert_status_code_in(status_code=[200, 201], message="success")
            self.request.assert_status_code_not_in(status_code=[404, 401], message="success")

        def test_assert_is_not_failed(self):
            self.request.assert_is_failed(message="request wasn't failed at all")

        def tearDown(self) -> None:
            return super().tearDown()


    suite = unittest.TestLoader().loadTestsFromTestCase(TestServices)
    output_file = open("report.html", "w")
    runner = HtmlTestRunner.HTMLTestRunner(
        stream=output_file,
        report_title="Test report"
    )
    runner.run(suite)

Custom assertion method
-----------------------

You can also create your own custom assertion method according to your need or case. To do that, you need to inherit the ``Http`` class from the client module and wrap it with your new assertion method. For example :

.. code-block:: python

    # custom_method.py
    from maritest.client import Http

    class MyCustomAssertion(Http):
        def assert_response_time_in_range(self, max_duration: int, end_duration: int):
            # assertion to check the response time is between range
            start_duration = 0

            while start_duration * max_duration <= end_duration:
                if self.response.elapsed.total_seconds() <= max_duration:
                    print(message)
                else:
                    message = "The duration exceeds the limit"
                    raise AssertionError(message)
            start_duration += 1

    # use your custom assertion
    response = MyCustomAssertion(
        method="GET",
        url="https://jsonplaceholder.typicode.com/posts/1",
        headers={},
        logger=True
    )
    response.assert_response_time_in_range(max_duration=200, end_duration=1200)

Caching API request after send
------------------------------

Sometimes you'll need caching the external API request after testing on it. In order to avoid the repetitive action without burdening the client side, you need to implement cache feature, to do that you need to install other package **cache-requests** to achieve this solution, for example :

.. code-block:: python

    # currently, we only patching the object and will be
    # cached entire of response without modified existing codebase
    import requests_cache
    from maritest.assert import Assert

    # simple configuration with SQLite3 as database
    # and will be flush after 180 seconds
    requests_cache.install_cache('custom_url_cache', backend='sqlite', expire_after=180)

    for index in range(100):
        response = Assert(
            method="GET",
            url=f"https://jsonplaceholder.typicode.com/posts/{index}",
            headers={}
        )

        response.assert_is_ok(message="should be success for all requests")
        response.assert_is_2xx_status(message="should be got 2xx status for all requests")

Integrate within Web Framework
------------------------------

If you tend run Maritest on-top of your favorite web framework (such as: Django or Flask), you can do to that by simply
write a instance class first for the Maritest wrapper, before it will be called in the APIs route.

For example, in here we will try to implemented in Flask

.. code-block:: python

    # app.py
    from flask import Flask, render_template, request
    from maritest.assertion import Assert

    app = Flask(__name__)

    # define the instance class first for Maritest
    class TestApiResponse:
        def get_status_codes(self, url, method, headers, message):
            assert_request = Assert(
                method=method,
                url=url,
                headers=headers
            )

            resp = assert_request.assert_is_ok(message=message)
            return response

    # now, define your flask route's
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            url = request.form["url"]
            method = request.form["method"]
            message = request.form["message"]
            headers = request.json
            maritest_instance = TestApiResponse()
            maritest_response = maritest_instance.get_status_codes(
                url, method, headers, message
            )

            result = {"status_code": maritest_response.status_code, "data": maritest_response.json()}

            # assuming that if you want to display the
            # Maritest result in client-side
            return render_template("index.html", result)
        return render_template("index.html")

    # now you can hit the Flask server and
    # see the result
    if __name__ == "__main__":
        app.run(debug=True)
