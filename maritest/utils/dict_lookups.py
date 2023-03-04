from typing import Union


def keys_in_dict(lookup: dict, keys=None) -> Union[bool, dict]:
    """
    Function to searching whether in any JSON response
    contains expected keys based on argument. This
    method can be used for searching keys in nested dict
    or only in single dict

    :param lookup: argument for set dictionary object
    :param keys: expected keys that want to be check
    """
    if keys is None:
        keys = []
    if not isinstance(lookup, dict):
        raise TypeError("argument lookup must be dict-object")

    current_dict = lookup
    for key in keys:
        if key in current_dict:
            current_dict.get(key)
            return True
        else:
            return False
    # return current_dict
