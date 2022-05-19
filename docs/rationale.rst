=================
Maritest Overview
=================

Rationale
---------

As the development process began to iterate quickly, QA teams need to step up again when writing automation tests, especially during assertions or schema validation while doing API testing

And thus it becomes problematic when many test scenarios need to be validated, especially from those scenarios that most likely will be written over-and-over again such as assertion for HTTP headers, response body, status code, or content-type. With **Maritest**, it will make it easier to write iterative assertions without the need for us to write again for the expectations and actual results from the API we tested and make it easier to maintainable API tests modules. From there, we can write it with much simpler automation API testing.
The most suitable depiction of what Maritest look alike and why is came up is to look at the following simple picture :


.. image:: https://i.ibb.co/p43YxtC/before-maritest.png
   :target: https://i.ibb.co/p43YxtC/before-maritest.png
   :alt: Before Maritest


Prior to **Maritest**, the process of testing or asserting HTTP targets / APIs endpoints would generally be collected into a single unit that we can call a "Test Suite". In the test suite itself there's a sub-class test which contains any scenarios that we need to test, but basically when we define a sub-class for that test scenario we will do the same process twice: 

- writing an assertion whether it failed, success or according our expectations 
- and write logic of test behind it.

Imagine if there are hundreds of API endpoints that need to be tested or in each of these API endpoints we want to do a different test, this lead to us become overwhelmed when writing it. And now, when using **Maritest** it become like this :

.. image:: https://i.ibb.co/7QX32J3/after-maritest.png
    :target: https://i.ibb.co/7QX32J3/after-maritest.png
    :alt: After Maritest

The ideation of Maritest is, we ended up wrapping our logic behind the test scenario and the assertion process into a single unit and made into a built-in assertion method that we can use as we wish. Basically, using Maritest also given incredible feat such as :

- avoids QA / Test Engineer from refactoring the test module process which is likely to get bigger in the future
- avoids implementing complex design patterns in early stage of development (such as using a Page Object Model or Facade) and keeping it stupid and simple 
- reduces tester time when write a lot of tests

Acknowledgments
---------------

- Maritest is built on top of the **requests** package to create the base HTTP client
- some of the built-in assertion methods provided by Maritest are inspired by the Postman script, Assertible or Blazemeter
- writing the assert syntax itself is also inspired by another package, namely **PyHamcrest**, a framework for writing matcher objects with declarative syntax

Limitation
----------

The main concern is about since our assertion is only limited to the assertions that we have defined previously, most likely it's very difficult to create and leverage other assertion scenarios that we wanted. Other than that, another problem is when you want to do custom validation in a complex response body, this library doesn't provided a method for that.

Another limitation is Maritest only supports 5 HTTP methods (GET, POST, PATCH, DELETE, PUT) and other HTTP methods are not supported yet and also some of the arguments that needed to make requests to the API are also missing, such as: 

- certification based on ``CA_BUNDLE`` file and CA certificates
- unable to streaming APIs request for download files
- intercept HTTP requests
- using Transport Adapters (although HTTP client for maritest was created with ``requests.Session()``, but i do not implement logic for the argument yet)
