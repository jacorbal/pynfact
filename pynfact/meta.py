# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Meta information processor from markdown post file.

Meta fields are set in English, Portuguese, Spanish, Catalan, Galician
and Esperanto (using the *X*-system), although there cannot be any
accent in the field names, so "título" has to be "titulo" in order to
work properly.

There may be diacritics in meta values (UTF-8 by default) but not in key
names (``[A-Za-z0-9]]``).

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
from dateutil.parser import parse
from pynfact.dataman import or_array_in
import datetime
import logging
import markdown
import re
import sys


class Meta:
    """Meta information processor.

    .. todo:: Use a general function retriever, instead of one function
        for each meta key.

    .. code-block:: python

        def process(self, array_of_valid_keys,
                type=[str, list, joined, date],
                date_format[if type is date]):

    * if ``type`` is ``"date"``, use the `date_format`
    * if ``type`` is ``"str"``, return the trimmed string as it comes
    * if ``type`` is ``"joined"``, return the list after splitting commas

    Code example of the intended feature::

        >>> m = Meta(meta_information)

        >>> title_valid_keys = ['title', 'titulo', 'titolo', 'titol' ]
        >>> def m.process(title_valid_keys, type='str')
        'The title to this Post'

        >>> date_valid_keys = ['date', 'data', 'dato', 'fecha' ]
        >>> def m.process(date_valid_keys, type='date', '%c')
        'Thu 12 Mar 2020 06:47:43 PM UTC'

        >>> tags_valid_keys = ['tags', 'labels', 'etiquetas', 'etikedoj']
        >>> def m.process(tags_valid_keys, type='join')
        ['tag1', 'tag2', 'tag3', 'tag4']

    .. versionchanged:: 1.3.1a3
        Validate source input meta tags of title (always) and date (when
        needed) raising a ``ValueError`` and passing to the logger the
        information of the error.
    """

    def __init__(self, meta, filename='', date_required=False,
                 logger=None):
        """Constructor.

        :param meta: Meta information dictionary
        :type meta: dict
        :param filename: Identifier for the file that is being tested
        :type filename: str
        :param date_required: If ``True`` checks for the date metadata
        :type date_required: bool
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        self.meta = meta
        self.logger = logger
        self.filename = filename
        self.date_required = date_required

        # Test if the data supplied is valid
        self.is_valid()

    def is_valid(self):
        """Check if the metadata is valid.

        The metadata is considered malformed when the title (and if
        ``date_required`` is set to ``True``, also the date) are not in
        the dictionary that is generated after parsing the file.  This
        could happen because:

        * title (or date) are missing;
        * title (or date) identifiers have invalid characters (the only
          valid ones are the ASCII character set encoded: "[A-Za-z0-9]");
        * title (or date) meta-information tag is more than one line
          long and it's not properly indented (subsequent lines require
          to be indented a minimum of four spaces).

        :return: ``False`` if problem found while getting the metadata
        :rtype: bool
        :raise ValueError: If the metadata is malformed

        .. versionadded:: 1.3.1a3
            Preliminary test to see if the mandatory meta tags are set,
            or otherwise an exception is thrown.
        """
        title_arr = ['titulo', 'title', 'titolo', 'entry', 'post', 'afiso']
        try:
            if not or_array_in(self.meta, *title_arr):
                raise ValueError
        except ValueError:
            self.logger and self.logger.error(
                'Missing or malformed title key in "{}" metadata'.format(
                    self.filename))
            sys.exit(31)

        if self.date_required:
            date_arr = ['fecha', 'date', 'data', 'dato']
            try:
                if not or_array_in(self.meta, *date_arr):
                    raise ValueError
            except ValueError:
                self.logger and self.logger.error(
                    'Missing or malformed date key in "{}" metadata'.format(
                        self.filename))
                sys.exit(32)

    def category(self, default_category='Miscellaneous'):
        """Get category as a string from post meta information.

        :return: Category field
        :rtype: str
        """
        category = self.meta.get('category') or \
            self.meta.get('categoría') or \
            self.meta.get('categoria') or self.meta.get('kategorio')
        return ' '.join(category) if category else default_category

    def author(self, default_author=''):
        """Get the author as a string from post meta information.

        .. todo:: If more than one author, return list, instead of
            ``str``.

        :return: Author field
        :rtype: str
        """
        authors = self.meta.get('authors') or self.meta.get('author') or \
            self.meta.get('autores') or self.meta.get('autors') or \
            self.meta.get('autor') or self.meta.get('autoro') or \
            self.meta.get('auxtoro')
        return ', '.join(authors) if authors else default_author

    def email(self):
        """Get the author's email as a string from post meta information.

        :return: Email field
        :rtype: str
        """
        emails = self.meta.get('email') or self.meta.get('e-mail') or \
            self.meta.get('correo electronico') or \
            self.meta.get('correo') or self.meta.get('correu') or \
            self.meta.get('e-correo') or \
            self.meta.get('retposto') or self.meta.get('retposxto')
        return ', '.join(emails) if emails else ''

    def language(self, default_language="en"):
        """Get the post language as a string from post meta information.

        :return: Language field
        :rtype: str
        """
        language = self.meta.get('language') or self.meta.get('idioma') or \
            self.meta.get('lengua') or self.meta.get('lingua') or \
            self.meta.get('llengua') or self.meta.get('lingvo')
        return language if language else default_language

    def title(self):
        """Get post title as a string from post meta information.

        :return: Title field
        :rtype: str
        """
        title = self.meta.get('title') or self.meta.get('titulo') or \
            self.meta.get('entry') or self.meta.get('entrada') or \
            self.meta.get('titol') or self.meta.get('post') or \
            self.meta.get('titolo')
        # return ''.join(title) if title else ''
        fmttitle = markdown.markdown(' '.join(title) if title else '')
        rtitle = re.sub(r'</*(p|br)[^>]*?>', '', fmttitle)

        try:
            if not rtitle:
                raise ValueError
        except ValueError:
            self.logger and self.logger.error(
                'Empty title value in "{}" metadata'.format(self.filename))
            sys.exit(33)

        return rtitle

    def summary(self):
        """Get post summary as a string from post meta information.

        :return: Summary field
        :rtype: str
        """
        summary = self.meta.get('summary') or self.meta.get('resumo') or \
            self.meta.get('resumen') or self.meta.get('resum')
        fmtsummary = markdown.markdown(' '.join(summary) if summary else '')
        return re.sub(r'</*(p|br)[^>]*?>', '', fmtsummary)

    def copyright(self):
        """Get post copyright as a string from post meta information.

        :return: Copyright field
        :rtype: str
        """
        copyright = self.meta.get('copyright') or \
            self.meta.get('license') or \
            self.meta.get('licencia') or \
            self.meta.get('licenza') or \
            self.meta.get('llicencia') or \
            self.meta.get('permesilo') or \
            self.meta.get('kopirajto') or \
            self.meta.get('(c)')
        fmtcopyright = markdown.markdown(' '.join(copyright) if copyright
                                         else '')
        return re.sub(r'</*(p|br)[^>]*?>', '', fmtcopyright)

    def date_info(self):
        """Get post date as a datetime object.

        :return: Date field
        :rtype: datetime
        """
        date = self.meta.get('date') or self.meta.get('data') or \
            self.meta.get('fecha') or self.meta.get('dato')
        return parse(''.join(date)) if date else ''

    def date(self, date_format='%c'):
        """Get post date as a string.

        :param date_format: Date locale
        :type date_format: str
        :return: Date field
        :rtype: str

        .. versionchanged:: 1.3.1a3
        Validate source input meta tags of date raising a ``ValueError``
        and passing to the logger the information of the error.
        """
        try:
            if not self.date_info():
                raise ValueError
        except ValueError:
            self.logger and self.logger.error(
                'Empty or invalid date value in "{}" metadata'.format(
                    self.filename))
            sys.exit(34)
        else:
            return self.date_info().strftime(date_format)

    def up_date_info(self):
        """Get updated post date as a datetime object.

        :return: Date field
        :rtype: datetime
        """
        up_date = self.meta.get('updated') or \
            self.meta.get('actualizado') or \
            self.meta.get('actualitzat') or \
            self.meta.get('gisdatigita') or \
            self.meta.get('gxisdatigita')
        return parse(''.join(up_date)) if up_date else ''

    def up_date(self, date_format='%c'):
        """Get updated post date as a string.

        :param date_format: Date locale
        :type date_format: str
        :return: Date field
        :rtype: str
        """
        return self.up_date_info().strftime(date_format) \
            if self.up_date_info() else ''

    def comments(self):
        """Get comments status.

        :return: True if entry has comments, or False otherwise
        :rtype: bool
        """
        comments = self.meta.get('comments') or \
            self.meta.get('comentarios') or \
            self.meta.get('comentaris') or \
            self.meta.get('komentoj') or ['']
        com_bool = False if comments[0].lower() == "no" or \
            comments[0].lower() == "non" or \
            comments[0].lower() == "não" or \
            comments[0].lower() == "ne" \
            else True
        return com_bool

    def private(self):
        """Get private status.

        :return: True if entry is private, or False otherwise
        :rtype: bool
        """
        private = self.meta.get('private') or \
            self.meta.get('privado') or \
            self.meta.get('privat') or \
            self.meta.get('privata') or ['']
        piv_bool = True if private[0].lower() == "yes" or \
            private[0].lower() == "si" or \
            private[0].lower() == "sí" or \
            private[0].lower() == "sim" or \
            private[0].lower() == "jes" \
            else False
        return piv_bool

    def navigation(self):
        """Get navigation status.

        :return: True if entry is navigable, or False otherwise
        :rtype: bool
        """
        navigation = self.meta.get('nav') or \
            self.meta.get('navigation') or \
            self.meta.get('navegacion') or \
            self.meta.get('navegacio') or \
            self.meta.get('navigado') or ['']
        nav_bool = False if navigation[0].lower() == "no" or \
            navigation[0].lower() == "non" or \
            navigation[0].lower() == "não" or \
            navigation[0].lower() == "ne" \
            else True
        return nav_bool

    def tag_list(self):
        """Get the tags as a list from post meta information.

        :return: List of tags
        :rtype: list
        """
        tag_list = self.meta.get('tags') or self.meta.get('labels') or \
            self.meta.get('etiquetas') or \
            self.meta.get('etiquetes') or \
            self.meta.get('etikedoj') or ['']
        tag_list = [x.strip() for x in tag_list[0].split(',') if x.strip()]
        return tag_list if tag_list else []

    def tags(self):
        """Get the tags as a list from post meta information.

        :return: List of tags
        :rtype: str
        """
        return ', '.join(tag_list(self.meta)) if tag_list(self.meta) else ''

    def __str__(self):
        """Return string representation for an object of this class."""
        return str(self.meta)

