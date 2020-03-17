# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
File and path manipulation functions.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""

from pynfact.struri import slugify, strip_html_tags
import os


def link_to(name, prefix='', makedirs=True, justdir=False,
            index='index.html'):
    """Make a link relative path in terms of the build.

    It may return a string to the destination, and also create that path
    if it doesn't exist. 

    :param name: Filename (extension will be disregarded)
    :type name: str
    :param prefix: Prefix directory to preppend the file
    :type prefix: str
    :param makedirs: If true make all needed directories
    :type makedirs: bool
    :param justdir: If true return only the link dir., not the full path
    :type justdir: bool
    :param index: Default name of file contained in the path
    :type index: str
    :return: Link path to a  ``index.html`` page
    :rtype: str

    :Example:

    >>> struri.link_to('dest', '/a/b/c', makedirs=False)
    '/a/b/c/dest/index.html'

    >>> struri.link_to('dest', 'a/b/c', makedirs=False, justdir=True)
    'a/b/c/dest'

    .. versionchanged:: 1.2.0a1
        Relocate function location from module :mod:`struri` to
        :mod:`fileman`.

    .. todo::
        Add a verbose argument, default to ``False`` (for
        compatibility), that prints status on creating the path if
        ``makedirs=True``.
    """
    dirname = slugify(strip_html_tags(os.path.splitext(name)[0]))
    path = os.path.join(prefix, slugify(dirname), index)
    if makedirs:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    return os.path.dirname(path) if justdir else path


def has_extension(filename, extension):
    """Test if the filename has a extension in particular.

    :param filename: Filename to test
    :type filname: str
    :param extension: Extension to test against
    :type extension: str
    :return: True if the filename has the inquired
    :rtype: bool
    """
    return os.path.splitext(filename)[1] == extension

