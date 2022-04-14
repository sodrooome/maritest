class JsonSerializer(dict):
    """
    Simple JSON-serializable class that only
    inherited from dict type built-ins. Most likely
    will works for all basic data representation (not)
    a complex one.

    :param json_object: Any object that which want
        to be formatted into JSON object

    Returned as a pair of key-value like JSON-type,
    empty argument will resulted as empty JSON
    """

    def __init__(self, object):
        if object is not None:
            dict.__init__(self, object=object)
