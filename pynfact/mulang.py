# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
    pynfact.mulang
    ~~~~~~~~~~~~~~

    Markdown translation to HTML and metadata "getter".

    :copyright: © 2012-2020, J. A. Corbal
    :license: MIT
"""
import markdown
import textwrap


class Mulang:
    """Generates HTML code from MarkUp LANGuage (mulang) source."""

    def __init__(self, input_data, encoding='utf-8',
                 output_format='html5', logger=None):
        """
        Initializer

        :param input_data: File from where the data is taken
        :type input_data: str
        :param encoding: Encoding the input file is in
        :type encoding: str
        :param output_format: Output HTML version
        :type output: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger

        This class has methods to parse the markup language and get the
        information.  The logging activity is only set to debug, since
        it's not neccessary to tell continously the default activity.
        """
        self.input_data = input_data
        self.encoding = encoding
        self.md = markdown.Markdown(
            extensions=['markdown.extensions.extra',
                        'markdown.extensions.toc',
                        'markdown.extensions.abbr',
                        'markdown.extensions.def_list',
                        'markdown.extensions.footnotes',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.meta'],
            encoding=encoding,
            output_format=output_format)
        self.logger = logger

    def html(self):
        """Generates HTML from Markdown data."""
        input_file = open(self.input_data, mode="r",
                          encoding=self.encoding)
        text = input_file.read()
        input_file.close()
        html = self.md.convert(text)

        self.logger and self.logger.debug('Parsed body data of: "%s"',
                                          self.input_data)

        return html

    def metadata(self):
        """Gets metadata in the markdown file.

        .. todo: Get the meta without generating HTML again
        """
        input_file = open(self.input_data, mode="r",
                          encoding=self.encoding)
        text = input_file.read()
        input_file.close()
        html = self.md.convert(text)

        self.logger and self.logger.debug('Parsed meta data of: "%s"',
                                          self.input_data)

        return self.md.Meta

