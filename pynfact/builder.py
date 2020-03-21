# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Build the content.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT

.. versionchanged:: 1.3.1a4
    Include processing of reStructuredText files along with Markdown.
    Those files are detected by extension and parsed accordingly.  So,
    no extension test in this module, only in the parser.

"""
from datetime import datetime
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader, Markup
from math import ceil
from pynfact.fileman import link_to
from pynfact.fileman import has_extension_md_rst as valid_ext
from pynfact.meta import Meta
from pynfact.parser import Parser
from pynfact.struri import slugify, strip_html_tags
import distutils.dir_util
import filecmp
import gettext
import locale
import os
import sys


class Builder:
    """Site building process manager.

    .. todo::
        Manage better the timezone, the default is always UTC, for posts
        info, and both feeds publication and modification dates.

    .. versionchanged:: 1.0.1.dev1
        Constructor takes a configuration dictionary instead of all
        parameters individually.

    .. versionchanged:: 1.0.1a1
        Input pages stored in ``pages`` directory instead of root.

    .. versionchanged:: 1.2.0a1
        Implement ``logging`` instead of printing to ``stdout`` and/or
        ``stderr``.

    .. versionchanged:: 1.3.1a4
        Allowed extension in constructor is no longer needed.  Input
        files are processed depending on their extension (Markdown or
        reStructuredText), and those are fixed.

    .. versionchanged:: 1.3.1b1
        Test of extension done by :func:`has_extension_md_rst` from
        module :mod:`fileman`.  No extensions passed as parameters nor
        defined explicitly in this class.

    .. versionchanged:: 1.3.1b1
        Feed is disabled if it has a value that doesn't match "rss" or
        "atom".  The templates will not generate the feed link in this
        particular case.
    """

    def __init__(self, site_config, template_values=dict(), logger=None):
        """Constructor.

        :param config: Site configuration as multidimensional dictionary
        :type config: dict
        :param template_values: Common values in all templates
        :type template_values: dict
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        :raise localeError: If the selected locale is not supported
        """
        self.site_config = site_config
        self.template_values = template_values
        self.site_config['dirs']['deploy'] = \
            os.path.join(self.site_config['dirs']['deploy'],
                         self.site_config['uri']['base'])
        self.logger = logger

        # Set locale for the site.
        self.old_locale = locale.getlocale()
        try:
            self.current_locale = \
                locale.setlocale(locale.LC_ALL,
                                 self.site_config['wlocale']['locale'])
        except locale.Error:
            self.logger and self.logger.error(
                "Unsupported locale setting")
            sys.exit(41)

        # Constants-like (I don't like this approach)
        # source dirs.
        self_dir = os.path.dirname(os.path.realpath(__file__))
        self.locale_dir = os.path.join(self_dir, 'data/locale')
        self.templates_dir = 'templates'
        self.builtin_templates_dir = \
            os.path.join(self.site_config['dirs']['deploy'],
                         self.templates_dir)

        # dest. dirs.
        self.home_cont_dir = 'page'         # Home paginator
        self.archive_dir = 'archive'        # Archive list page
        self.categories_dir = 'categories'  # One dir. per category
        self.tags_dir = 'tags'              # One dir. per tag

        # src. & dest. dirs.
        self.pages_dir = 'pages'            # Other pages such as 'About'...
        self.entries_dir = 'posts'          # Where posts are
        self.static_dir = 'static'          # CSS, JS, &c.

        # Default values to override meta information
        self.meta_defaults = {
            'author': self.site_config['info']['site_author'],
            'category': self.site_config['presentation']['default_category'],
        }

    def __del__(self):
        """Destructor.  Restore the locale, if changed."""
        return locale.setlocale(locale.LC_ALL, self.old_locale)

    def gen_entry(self, infile, date_format='%c'):
        """Generate a HTML entry from its Markdown counterpart.

        :param infile: Markdown file to parse
        :type infile: str
        :param date_format: Date format for entry
        :type date_format: str
        :return: Generated HTML
        :rtype: str
        """
        meta = self._fetch_meta(self.entries_dir, infile, True)
        html = self._fetch_html(self.entries_dir, infile)

        override = {
            'category_uri': self._make_root_uri(meta.category(),
                                                self.categories_dir),
            'content': html,
            'site_comments': self.site_config['presentation']['comments'],
        }
        values = self.template_values.copy()
        values['entry'] = meta.as_dict(override, self.meta_defaults,
                                       date_format)
        outfile = self._make_output_file(
            values['entry']['title'], self._entry_link_prefix(infile))

        return self._render_template('entry.html.j2', outfile, values)

    def gen_entries(self, date_format='%c'):
        """Generate all entries.

        :param date_format: Date format for entry
        :type date_format: str
        """
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                self.gen_entry(filename, date_format=date_format)

    def gen_home(self, max_entries_per_page=10, date_format='%Y-%m-%d'):
        """Generate home page, and subpages.

        :param max_entries: Max. entries per page
        :type max_entries: int
        :param date_format: Date format for home page
        :type date_format: str
        """
        entries = list()
        total_entries = 0
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)

                override = {
                    'category_uri': self._make_root_uri(meta.category(),
                                                        self.categories_dir),
                    'odate_idx': meta.odate('%Y-%m-%d %H:%M:%S'),
                    'uri': self._make_entry_uri(meta.title(),
                                                filename,
                                                absolute=True),
                }

                # Generate entries list
                if not meta.private():
                    total_entries += 1
                    entries.append(meta.as_dict(override,
                                                self.meta_defaults,
                                                date_format))

        # Sort chronologically descent
        entries = sorted(entries, key=lambda k: k['odate_idx'],
                         reverse=True)

        total_pages = ceil(total_entries / max_entries_per_page)
        values = self.template_values.copy()

        # FIXME: Generate 'index.html' even when there are no posts
        if total_entries == 0:
            outfile = self._make_output_file()
            self._render_template('entries.html.j2', outfile, values)

        # Home page (and subsequent ones)
        for cur_page in range(1, total_pages + 1):
            min_page = (cur_page - 1) * max_entries_per_page
            max_page = cur_page * max_entries_per_page

            values['entries'] = entries[min_page:max_page]
            values['cur_page'], values['total_pages'] = \
                cur_page, total_pages

            if cur_page == 1:
                # This is the home page, the "index.html" of the site
                outfile = self._make_output_file()
            else:
                # These are the subsequent pages other than the first
                outfile = self._make_output_file(
                    str(cur_page), self.home_cont_dir)
            self._render_template('entries.html.j2', outfile, values)
            values['entries'] = {}  # reset the entries dict.

    def gen_archive(self, date_format='%c'):
        """Generate complete website archive, based on date.

        :param date_format: Date format for entry
        :type date_format: str
        """
        archive = dict()
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)

                override = {
                    'category_uri': self._make_root_uri(meta.category(),
                                                        self.categories_dir),
                    'uri': self._make_entry_uri(meta.title(),
                                                filename),
                    'odate_idx': meta.odate('%Y-%m-%d'),
                }

                # Generate archive
                if not meta.private():
                    val = meta.as_dict(override, self.meta_defaults,
                                       date_format)
                    oyear_idx = meta.odate('%Y')
                    # '%m-%d' to sort chronologically
                    omonth_idx = meta.odate('%m-%d')
                    if oyear_idx in archive:
                        if omonth_idx in archive[oyear_idx]:
                            archive[oyear_idx][omonth_idx].append(val)
                        else:
                            archive[oyear_idx][omonth_idx] = [val]
                        # sort entries
                        archive[oyear_idx][omonth_idx] = \
                            sorted(archive[oyear_idx][omonth_idx],
                                   key=lambda k: k['odate_idx'],
                                   reverse=False)
                    else:
                        archive[oyear_idx] = dict()
                        archive[oyear_idx][omonth_idx] = [val]

        values = self.template_values.copy()
        values['archive'] = archive
        outfile = self._make_output_file('', self.archive_dir)
        return self._render_template('archive.html.j2', outfile, values)

    def gen_category_list(self, date_format='%c'):
        """Generate categories page (an archive sorted by category).

        :param date_format: Date format for entry
        :type date_format: str
        """
        archive = dict()
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)

                override = {
                    'uri': self._make_entry_uri(meta.title(), filename),
                    'odate_idx': meta.odate('%Y-%m-%d'),
                }

                # Generate archive
                if not meta.private():
                    val = meta.as_dict(override, self.meta_defaults,
                                       date_format)
                    category = meta.category()
                    if category in archive:
                        archive[category].append(val)
                    else:
                        archive[category] = [val]
                    # sort entries
                    archive[category] = \
                        sorted(archive[category],
                               key=lambda k: k['odate_idx'],
                               reverse=True)

        values = self.template_values.copy()
        values['archive'] = archive
        outfile = self._make_output_file('', self.categories_dir)
        return self._render_template('catlist.html.j2', outfile, values)

    def gen_categories(self, date_format='%c'):
        """Generate categories pages.

        :param date_format: Date format for entry
        :type date_format: str
        """
        entries_by_category = dict()
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)

                override = {
                    'odate_idx': meta.odate('%Y-%m-%d'),
                    'uri': self._make_entry_uri(meta.title(), filename),
                }

                # Generate dictionary of entries by category
                if not meta.private():
                    val = meta.as_dict(override, self.meta_defaults,
                                       date_format)
                    category = meta.category()
                    if category in entries_by_category:
                        entries_by_category[category].append(val)
                    else:
                        entries_by_category[category] = [val]

        # One page for each category
        values = self.template_values.copy()
        for category in entries_by_category:
            values['category_name'] = category
            values['entries'] = entries_by_category[category]
            # sort entries
            values['entries'] = sorted(values['entries'], key=lambda k:
                                       k['odate_idx'], reverse=True)
            outfile = self._make_output_file(category, self.categories_dir)
            self._render_template('cat.html.j2', outfile, values)

    def gen_tags(self, date_format='%c'):
        """Generate tags pages.

        :param date_format: Date format for entry
        :type date_format: str
        """
        entries_by_tag = dict()
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)

                override = {
                    'odate_idx': meta.odate('%Y-%m-%d'),
                    'uri': self._make_entry_uri(meta.title(), filename),
                }

                # Generate dictionary of entries by tag
                if not meta.private():
                    val = meta.as_dict(override, self.meta_defaults,
                                       date_format)
                    for tag in meta.tag_list():
                        if tag in entries_by_tag:
                            entries_by_tag[tag].append(val)
                        else:
                            entries_by_tag[tag] = [val]

        # One page for each tag
        values = self.template_values.copy()
        for tag in entries_by_tag:
            values['tag_name'] = tag
            values['entries'] = entries_by_tag[tag]
            # sort entries
            values['entries'] = sorted(values['entries'], key=lambda k:
                                       k['odate_idx'], reverse=True)
            outfile = self._make_output_file(tag, self.tags_dir)
            self._render_template('tag.html.j2', outfile, values)

    def gen_tag_cloud(self):
        """Generate tags cloud page.

        Tags will appear in different sizes depending on the their
        occurrences along the posts.  The more a tag is used, the bigger
        will be displayed.
        """
        entries_by_tag = dict()
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)

                # Generate dictionary of entries by tag
                if not meta.private():
                    val = meta.as_dict({}, self.meta_defaults)
                    for tag in meta.tag_list():
                        if tag in entries_by_tag:
                            entries_by_tag[tag].append(val)
                        else:
                            entries_by_tag[tag] = [val]

        # Multipliers seq. for tag size in function of times repeated
        tagcloud_seq = [0, 14, 21, 27, 32, 38, 42, 45, 47, 48, 50, 52]

        # One page for each tag
        values = self.template_values.copy()
        values['tags'] = []
        for tag in entries_by_tag:
            if tag:
                tagname, tagfreq = tag, len(entries_by_tag[tag])
                mult = 100 + int(tagcloud_seq.last
                                 if tagfreq > len(tagcloud_seq)
                                 else tagcloud_seq[tagfreq - 1])
                values['tags'].append({tagname: mult})

        outfile = self._make_output_file('', self.tags_dir)
        self._render_template('tagcloud.html.j2', outfile, values)

    def gen_nav_page_links(self):
        """Update the template data to contain also all page links.

        The navigation bar contains, not all links relevant to the site,
        but also all pages without the meta descriptor ``Navigate`` set
        to "no".

        .. important::
            Since this add new data to the base template, it **must be
            invoked first**, before generating any other content.
        """
        for filename in os.listdir(self.pages_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.pages_dir, filename, False)

                override = {'uri': self._make_root_uri(meta.title())}

                if meta.navigation():
                    values = self.template_values.copy()
                    values['page'] = meta.as_dict(override,
                                                  self.meta_defaults)

                    # Update base template values to get pages links in
                    # nav. bar only if the page is set to be in the
                    # navigation bar
                    self.template_values['blog']['page_links'].append(
                        [values['page']['title'],
                         values['page']['uri']])

                    self.logger and self.logger.info(
                        'Added page to navigation: "{}"'.format(filename))

    def gen_page(self, infile):
        """Generate a HTML page from its Markdown counterpart.

        :param infile: Markdown file to parse
        :type infile: str
        :return: Generated HTML
        :rtype: str
        """
        meta = self._fetch_meta(self.pages_dir, infile, False)
        html = self._fetch_html(self.pages_dir, infile)

        override = {'content': html}

        values = self.template_values.copy()
        values['page'] = meta.as_dict(override, self.meta_defaults)

        outfile = self._make_output_file(meta.title())
        return self._render_template('page.html.j2', outfile, values)

    def gen_pages(self):
        """Generate all pages."""
        for filename in os.listdir(self.pages_dir):
            if valid_ext(filename):
                self.gen_page(filename)

    def gen_feed(self, feed_format="atom", outfile='feed.xml'):
        """Generate blog feed.

        :param feed_format: Feed format string ('rss' or 'atom').
                            If invalid value, will default to 'atom'
        :type feed_format: str
        :param outfile: Output filename
        :type outfile: str
        """
        if feed_format.lower() != "atom" and \
           feed_format.lower() != "rss":
            return

        feed = FeedGenerator()
        # feed.logo()
        feed.id(self.site_config['info']['site_name']
                if self.site_config['info']['site_name']
                else self.site_config['uri']['canonical'])
        feed.title(self.site_config['info']['site_name']
                   if self.site_config['info']['site_name']
                   else self.site_config['uri']['canonical'])
        feed.subtitle(self.site_config['info']['site_description']
                      if self.site_config['info']['site_description']
                      else 'Feed')
        feed.author({'name': self.site_config['info']['site_author'],
                     'email': self.site_config['info']['site_author_email']})
        feed.description(self.site_config['info']['site_description'])
        feed.link(href=os.path.join(self.site_config['uri']['canonical'],
                                    self.site_config['uri']['base']),
                  rel='alternate')
        feed.link(href=os.path.join(self.site_config['uri']['canonical'],
                                    self.site_config['uri']['base'],
                                    outfile), rel='self')
        feed.language(self.site_config['wlocale']['language'])
        feed.copyright(self.site_config['info']['copyright'])

        entries = list()
        for filename in os.listdir(self.entries_dir):
            if valid_ext(filename):
                meta = self._fetch_meta(self.entries_dir, filename, True)
                html = self._fetch_html(self.entries_dir, filename)

                uri = self._make_entry_uri(meta.title(), filename)
                override = {
                    'content_html': html,
                    'full_uri': os.path.join(self.site_config['uri']['canonical'],
                                             self.site_config['uri']['base'], uri),
                    'mdate_idx': meta.mdate('%Y-%m-%d %H:%M:%S'),
                    'odate_idx': meta.odate('%Y-%m-%d %H:%M:%S'),
                    'timezone': 'UTC' if not meta.odate('%Z')
                    else meta.odate('%Z'),
                    'uri': uri,
                }

                if not meta.private():
                    val = meta.as_dict(override, self.meta_defaults)
                    entries.append(val)

        # Sort chronologically descent
        entries = sorted(entries, key=lambda k: k['odate_idx'],
                         reverse=True)
        for entry in entries:
            fnew = feed.add_entry()
            fnew.id(slugify(strip_html_tags(entry['title'])))
            fnew.title(entry['title'])
            fnew.description(entry['content_html'])
            if entry['mdate_html']:
                fnew.updated(entry['mdate_html'])
                fnew.published(entry['mdate_html'])
            else:
                fnew.updated(entry['odate_html'])
            fnew.pubDate(entry['odate_html'])
            # , 'email':entry['email']})
            fnew.author({'name': entry['author']})
            fnew.link(href=entry['full_uri'], rel='alternate')

        if feed_format.lower() == "rss":
            feed.rss_file(os.path.join(self.site_config['dirs']['deploy'],
                                       outfile))
        elif feed_format.lower() == "atom":
            feed.atom_file(os.path.join(self.site_config['dirs']['deploy'],
                                        outfile))

    def gen_static(self):
        """Generate (copies) static directory."""
        src = self.static_dir
        dst = os.path.join(self.site_config['dirs']['deploy'],
                           self.static_dir)
        if os.path.exists(src):
            distutils.dir_util.copy_tree(src, dst, update=True,
                                         verbose=True)

    def gen_extra_dirs(self):
        """Generate extra directories if they exist."""
        if self.site_config['dirs']['extra']:
            for extra_dir in self.site_config['dirs']['extra']:
                src = extra_dir
                dst = os.path.join(self.site_config['dirs']['deploy'],
                                   extra_dir)
                if os.path.exists(src):
                    distutils.dir_util.copy_tree(src, dst, update=True,
                                                 verbose=True)

    def gen_site(self):
        """Generate all website content.

        .. note::
            The first thing that has to be generated is the navigation
            links for all user defined pages.  Otherwise those links
            could be left behind on page pages.
        """
        self.logger and self.logger.info('Building static website...')

        self.gen_nav_page_links()
        self.gen_entries(self.site_config['date_format']['entry'])
        self.gen_pages()
        self.gen_archive(self.site_config['date_format']['list'])
        self.gen_categories(self.site_config['date_format']['list'])
        self.gen_category_list(self.site_config['date_format']['list'])
        self.gen_tags(self.site_config['date_format']['list'])
        self.gen_tag_cloud()
        self.gen_home(self.site_config['presentation']['max_entries'],
                      self.site_config['date_format']['home'])
        self.gen_feed(self.site_config['presentation']['feed_format'])
        self.gen_static()
        self.gen_extra_dirs()

        self.logger and self.logger.info('Done!')

    def _render_template(self, template, output_data, values):
        """Render a template using Jinja2.

        :param template: Template to use
        :type template: str
        :param output_data: File where the data is saved
        :type output_data: str
        :return: Generated HTML of the output data
        :rtype: str
        """
        trans = gettext.translation('default', self.locale_dir,
                                    [self.current_locale])
        env = Environment(extensions=['jinja2.ext.i18n'],
                          loader=FileSystemLoader([self.templates_dir,
                                                   self.builtin_templates_dir]))
        env.install_gettext_translations(trans)
        env.globals['slugify'] = slugify  # Add `slugify` to Jinja2
        env.globals['strip_html_tags'] = strip_html_tags
        template = env.get_template(template)
        html = template.render(**values)

        # Update only those files that are different in content
        # comparing with a cache file
        with open(output_data + '~', mode="w",
                  encoding=self.site_config['wlocale']['encoding']) \
                as cache_file:
            cache_file.write(html)

        if not os.path.exists(output_data) or \
           not filecmp.cmp(output_data + '~', output_data):
            with open(output_data, mode="w",
                      encoding=self.site_config['wlocale']['encoding']) \
                    as output_file:
                output_file.write(html)
            self.logger and self.logger.info(
                'Updated content of: "{}"'.format(output_data))

        # Clear cache, both in memory and space
        filecmp.clear_cache()
        os.remove(output_data + '~')

        return html

    def _fetch_markup(self, directory, infile):
        """Parse an input file depending on its extension.

        The ``Parser`` constructor detects the extension of ``infile``
        and parses its body content as well as its metadata.

        :param directory: Path to the file to be parsed
        :type directory: str
        :param infile: File to parse
        :type infile: str
        :return: Parser object
        :rtype: Parser

        .. sealso:: :class:`Parser`
        """
        return Parser(os.path.join(directory, infile),
                      encoding=self.site_config['wlocale']['encoding'],
                      logger=self.logger)

    def _fetch_html(self, directory, infile):
        """Fetch HTML content out of a Markdown input file.

        :param directory: Markdown file working directory
        :type directory: str
        :param infile: Markdown file to parse
        :type infile: str
        :return: HTML content for the parsed file
        :rtype: str
        """
        return self._fetch_markup(directory, infile).html()

    def _fetch_meta(self, directory, infile, odate_required=False):
        """Fetch metadata out of a Markdown input file.

        If ``odate_required`` is ``False``, the metadata is valid as
        long as it has a title; if it's ``True``, the metadata require
        to be valid, also an "origin date", or ``odate`` field.

        :param directory: Markdown file working directory
        :type directory: str
        :param infile: Markdown file to parse
        :type infile: str
        :param odate_required: Field ``odate`` is required
        :type odate_required: bool
        :return: Markdown metadata
        :rtype: Meta
        """
        return Meta(self._fetch_markup(directory, infile).metadata(),
                    infile, odate_required, logger=self.logger)

    def _entry_link_prefix(self, entry):
        """Compute entry final path.

        To compute the final path, it's required to take the meta
        information of that entry concerning to title and origin date.
        Let's suppose the title is "My post", and the ``odate`` set to
        "2020-04-01".  The output will be: ``posts/2020/04/01/my-post``.

        :param: Entry filename
        :type: str
        :return: Path to this entry relative to root (slugified)
        :rtype: str

        .. versionchanged:: 1.3.0a
            Set as a member method.
        """
        meta = self._fetch_meta(self.entries_dir, entry, True)

        category = meta.category(
            self.site_config['presentation']['default_category'])
        odate = meta.odate('%Y-%m-%d')
        odate_arr = odate.split('-')
        path = os.path.join(str(self.entries_dir),
                            slugify(category),
                            str(odate_arr[0]),
                            str(odate_arr[1]),
                            str(odate_arr[2]))
        return path

    def _make_entry_uri(self, name='', infix='', index='index.html',
                        absolute=False):
        """Generate the link to an entry, based on the date and name.

        Link automated generation for final URIs of articles.

        :type name: Destination basename
        :param name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :param absolute: Force the URI to be done from the root
        :type absolute: bool
        :return: Link to final external URI relative to root directory
        :rtype: str
            .
        """
        if absolute:
            path = os.path.join('/',
                                self.site_config['uri']['base'],
                                self._entry_link_prefix(infix))

        else:
            path = self._entry_link_prefix(infix)

        return link_to(name, path, makedirs=False, justdir=True,
                       index=index)

    def _make_root_uri(self, name='', infix='', index='index.html'):
        """Generate the link to any resource in the root file system.

        Link automated generation for final URIs of the content in
        the website root directory, such as pages.

        :type name: Destination basename
        :param name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :return: Link to final external URI relative to root directory

        .. versionadded:: 1.3.2a

        """
        return link_to(name,
                       os.path.join('/',
                                    self.site_config['uri']['base'],
                                    infix),
                       makedirs=False, justdir=True, index=index)

    def _make_output_file(self, name='', infix='', index='index.html'):
        """Return the output file link, and make required directories.

        Link automated generation for files in the deploy directory.

        :param name: Destination basename
        :type name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :return: Link to the constructed path in the deploy directory
        :rtype: str
        """
        return link_to(name,
                       os.path.join(self.site_config['dirs']['deploy'],
                                    infix),
                       makedirs=True, justdir=False, index=index)

