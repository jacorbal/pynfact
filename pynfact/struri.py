# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
URI strings manipulation functions.

    :copyright: © 2012-2020, J. A. Corbal
    :license: MIT
"""
import unidecode
import re


def slugify(unslugged, separator='-'):
    """Slug a string.

    :param unslugged: String to slugify
    :type unslugged: str
    :param separator: Character used to separate words
    :type separator: str
    :return: Slugged string
    :rtype: str
    """
    return re.sub(r'\W+', separator,
                  unidecode.unidecode(unslugged).strip().lower())


def strip_html_tags(text):
    """Strip HTML tags in a string.

    :param text: String containing HTML code
    :type text: str
    :return: String without HTML tags
    :rtype: str
    """
    return re.sub('<[^<]+?>', '', text)

