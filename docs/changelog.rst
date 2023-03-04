=========
Changelog
=========

All of this changelog are based on the release history like published in https://pypi.org/project/maritest/#history

**v0.6.0**
------------------------

- [Fixed] Change parameter option name of ``format`` to ``fmt`` in ``retriever`` method
- [Fixed] Option to choose ``content`` response as argument when use ``retriever`` method
- [Fixed] Attribute instance of ``timeout`` parameter can't be use
- [Fixed] Duplicate logger stream output when enable ``logger`` parameter
- [Added] New properties method to quick access HTTP response object
- [Improvement] Change duration timeout into random numbers whenever set to ``None``
- [Improvement] Major refactoring in core APIs for simplifying redundant and unused codes
- [Improvement] ``headers`` parameter now is optional when try to request HTTP
- **[Known Issue]** Setup HTTP with proxy parameter sometimes will get error related to remote end close connection.
- **[Known Issue]** Logger will run hierarchy in another function / class even though the logger has been disabled


**v0.5.1**
----------

- [Fixed] Error raises when call ``__exit__`` using context manager
- [Fixed] Can't decode into JSON format due conflicted with JSON serializer class
- [Fixed] Exception error when caught invalid JSON format
- [Fixed] Disabling ``logger`` argument not writing log information in files output
- [Improvement] Separated between log information before-after send HTTP request

**v0.5.0**
----------

- [Fixed] Attribute object of  ``auth``, ``data`` , ``params`` and ``files`` needs to be called in argument
- [Fixed] Remove unused ``raise_for_status`` method when raise error
- [Fixed] Remove duplicate logger warning and move the logger after response is success
- [Fixed] Method property to get ``url`` not returned with full-path ``url``
- [Fixed] Remove setter-getter method to returned HTTP method value
- [Fixed] Invalid log warning raises when mounted HTTPS protocol
- [Fixed] Change validation assertion for ``2xx`` status code
- [Fixed] Method whitelist for retry HTTP request not correct
- [Fixed] User authentication flow invalid when using ``ApiKeyAuth`` method
- [Fixed] Failed request got 400 status when send with ``data`` argument
- [Improvement] Caught exception error when mapping for key and unpacking key-value in HTTP response not found
- [Improvement] Delete all related HTTP adapters and close the connection

**v0.4.0**
----------

- [Improvement] Add ``logger`` file handler when disable the log
- [Added] New 2 assertion method, check content-length and check TLS
- [Fixed] Value for ``ApiKeyAuth`` authentication should be customized
- [Fixed] Annotation for ``ApiKeyAuth`` violates LSP from parent class

**v0.3.2**
----------

- [Fixed] Missing validation when send request for ``files`` and ``json``
- **[Known Issue]** Response got 400 status when send ``data`` with ``headers``
    
**v0.3.1**
----------

- [Improvement] Always enforce response encoding set to UTF-8
- [Fixed] Duplicate assertion test for validate content text
- [Fixed] Remove lambda operator in function

**v0.3.0**
----------

- [Added] Invoke ``auth`` argument now callable through parameter
- [Added] New method for returned raw HTTP response
- [Added] New method for using HTTP authentication
- [Fixed] HTTP scheme raise unexpectedly when using HTTPS protocol
- [Fixed] Error parse for URL when using HTTP protocol
- [Improvement] Documentation for better user reading

**v0.2.1**
----------

- [Fixed] JSON object need to be dumps first before making assertion
- [Fixed] Can't import relative module

**v0.2.0**
----------

- [Added] New method for returned formatted HTTP response (JSON, binary, content)
- [Added] New assertion method for testing
- [Improvement] Documentation for better user reading
- [Improvement] Enable timeout for handling error due proxy
- [Fixed] Validation for valid or invalid URL scheme
- [Fixed] Validation for HTTP mounted adapter
- [Fixed] Suppression warning error falsely mistaken to ``True``
- [Fixed] Rename ``proxies`` parameter due conflict naming

**v0.1.0**
----------

- Moving to public repo and initial release for **Maritest**
