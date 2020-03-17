# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Data and data structures management functions.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. versionadded:: 1.3.1a3
    Separate funcionality across multiple modules.
"""


def or_array_in(dictionary, *keys):
    """Check if at least one key in the array is in the dictionary.

    The funcionality is the same as the keyword ``in``, but testing each
    and every key in the array as an ``or`` operation.

    :param keys: List of keys to test against the dictionary
    :type keys: args
    :param dictionary: Dictionary
    :type dictionary: dict
    :return: ``True`` if at least one key is in the dictionary
    :rtype: bool
    """
    for key in keys:
        if key in dictionary:
            return True

    return False


def and_array_in(dictionary, *keys):
    """Check if every key in the array is in the dictionary.

    The funcionality is the same as the keyword ``in``, but testing each
    and every key in the array as an ``and`` operation.

    :param keys: List of keys to test against the dictionary
    :type keys: args
    :param dictionary: Dictionary
    :type dictionary: dict
    :return: ``True`` if at all keys are in the dictionary
    :rtype: bool
    """
    for key in keys:
        if key not in dictionary:
            return False

    return True


def keys_exists(dictionary, *keys):
    """Check if nested keys exist in a dictionary.
    
    :param dictionary: Nested dicionary
    :type dictionary: dict
    :param keys: Keys to test agains the dictionary
    :type keys: args
    :return: ``True`` if at least one key is in the dicionary
    :rtype: bool
    :raise KeyError: If no key is in the dictionary
    """
    item = dictionary
    for key in keys:
        try:
            item = item[key]
        except KeyError:
            return False
    return True

