# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Markdown translation to HTML and metadata retrieval.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
from pynfact.fileman import has_extension_md, has_extension_rst
from pynfact.parsers import ParserMd
from pynfact.parsers import ParserRst


class Parser:
    """Parse methods for a markup language file to generate HTML code.

    .. versionchanged:: 1.3.1b1
        Former class ``Mulang``, now it relies on the file extension to
        call one or other parser.
    """

    def __init__(self, input_data, encoding='utf-8', logger=None):
        """Constructor.

        Depending on the extension, the markup parser will be a Markdown
        parser, or a reStructuredText parser.  The valid extensions are:
        ``.rst`` for reStructuredText, and ``.md`` for Markdown.

        :param input_data: File from where the data is taken
        :type input_data: str
        :param encoding: Encoding the input file is in
        :type encoding: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        """
        #Parser = ParserRst if has_extension_rst(input_data) else ParserMd
        if has_extension_rst(input_data):
            Parser = ParserRst
        elif has_extension_md(input_data):
            Parser = ParserMd

        self.parser = Parser(input_data, encoding, logger=logger)

    def html(self):
        """Generate HTML from a MarkUP LANGuage file."""
        return self.parser.html()

    def metadata(self):
        """Generate metadata from a MarkUP LANGuage file."""
        return self.parser.metadata()

