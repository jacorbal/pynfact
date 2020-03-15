# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Build the content.

Only markdown files will be taken, but markdown files are identified by
its extension, which for this application is ``.md`` (but it may be
specified in ``infile_ext`` argument)

    :copyright: © 2012-2020, J. A. Corbal
    :license: MIT
"""
from datetime import datetime
from feedgen.feed import FeedGenerator
from jinja2 import Environment, FileSystemLoader, Markup
from math import ceil
from pynfact.fileman import link_to, has_extension
from pynfact.meta import Meta
from pynfact.mulang import Mulang
from pynfact.struri import slugify, strip_html_tags
import distutils.dir_util
import filecmp
import gettext
import locale
import os
import sys
import textwrap


class Builder:
    """Site building process manager.

    .. todo:: Manage better with timezones. Make sure if there is no
              timezone, the default is always UTC, for posts info, and
              both feeds publication and modification dates.

    .. todo:: Remove redundant code using a universal method for
              retrieve and gather the data; and use subclasses.

    .. todo:: Unlink all file management from this class and build
              andother module to deal with that

    .. versionchanged:: 1.0.1.dev1
       Constructor takes a configuration dictionary instead of all
       parameters individually

    .. versionchanged:: 1.0.1a1
       Input pages stored in ``pages`` directory instead of root

    .. versionchanged:: 1.2.0a1
       Implement ``logging`` instead of printing to ``stdout`` and/or
       ``stderr``

    """

    def __init__(self, site_config, template_values=dict(),
                 infile_ext='.md', logger=None):
        """Constructor.

        :param config: Site configuration as multidimensional dictionary
        :type config: dict
        :param template_values: Common values in all templates
        :type template_values: dict
        :param infile_ext: Posts files extension
        :type infile_ext: str
        :param logger: Logger where to store activity in
        :type logger: logging.Logger
        :raise: localeError
        """
        self.site_config = site_config
        self.template_values = template_values
        self.infile_ext = infile_ext.lower()
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
        self.locale_dir = os.path.join(self_dir, 'locale')
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

    def __del__(self):
        """Destructor.  Restore the locale, if changed."""
        return locale.setlocale(locale.LC_ALL, self.old_locale)

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
                'Updated content of: "%s"', output_data)

        # Clear cache, both in memory and space
        filecmp.clear_cache()
        os.remove(output_data + '~')

        return html

    def _entry_link_prefix(self, entry):
        """Compute entrie final path.

        To compute the final path, it's required to take the meta
        information of that entry concerning to title and publication
        date.
        Let's suppose the title is "My entry", and the date is
        "2020-04-01".  The output will be: `posts/2020/04/01/my-entry`

        :param: Entry filename
        :type: str
        :return: Path to this entry relative to root (slugified)
        :rtype: str
        """
        meta = Meta(Mulang(os.path.join(self.entries_dir, entry),
                           self.site_config['wlocale']['encoding'],
                           logger=self.logger).metadata())
        category = meta.category(
            self.site_config['presentation']['default_category'])
        date = meta.date('%Y-%m-%d')
        date_arr = date.split('-')
        path = os.path.join(str(self.entries_dir),
                            slugify(category),
                            str(date_arr[0]),
                            str(date_arr[1]),
                            str(date_arr[2]))
        return path

    def _make_entry_uri(self, name='', infix='', index='index.html',
                        force_root=False):
        """Generate the link to an entry, based on the date and name.

        :type name: Destination basename
        :param name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :param force_root: Force the URI to be done from the root
        :type force_root: bool
        :return: Link to final external URI relative to root directory
        :rtype: str
        """
        if force_root:
            return link_to(name,
                           os.path.join('/',
                                        self.site_config['uri']['base'],
                                        self._entry_link_prefix(infix)),
                           makedirs=False, justdir=True, index=index)
        else:
            return link_to(name,
                           self._entry_link_prefix(infix),
                           makedirs=False, justdir=True, index=index)

    def _make_root_uri(self, name='', infix='', index='index.html'):
        """Generate the link to any resource in the root filesystem.

        :type name: Destination basename
        :param name: str
        :param infix: Appendix to the deploy directory
        :type infix: str
        :param index: Default name of the generated resource
        :type index: str
        :return: Link to final external URI relative to root directory
        """
        return link_to(name,
                       os.path.join('/',
                                    self.site_config['uri']['base'],
                                    infix),
                       makedirs=False, justdir=True, index=index)

    def _make_output_file(self, name='', infix='', index='index.html'):
        """Return the output file link, and make required directories.

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
                       os.path.join(self.site_config['dirs']['deploy'], infix),
                       makedirs=True, justdir=False, index=index)

    def gen_entry(self, infile, date_format='%c'):
        """Generate a HTML entry from its Mardkdown counterpart.

        :param infile: Markdown file to parse
        :type infile: str
        :param date_format: Date format for entry
        :type date_format: str
        :return: Generated HTML
        :rtype: str
        """
        inpath = os.path.join(self.entries_dir, infile)
        ml = Mulang(inpath, self.site_config['wlocale']['encoding'],
                    logger=self.logger)
        meta = Meta(ml.metadata())
        content_html = ml.html()

        title = meta.title()
        category = meta.category(
            self.site_config['presentation']['default_category'])
        timezone = meta.date('%z')
        if timezone:
            # to html5 timezone conv.
            timezone = timezone[:3] + ':' + timezone[3:]
        datehtml = meta.date('%Y-%m-%dT%H:%M') + timezone
        up_datehtml = meta.up_date('%Y-%m-%dT%H:%M') \
            + timezone if meta.up_date('%Y-%m-%dT%H:%M') \
                       else None

        values = self.template_values.copy()
        values['entry'] = {  # append
            'author': meta.author() \
            if meta.author() \
            else self.site_config['info']['site_author'],
            'title': title,
            'raw_title': strip_html_tags(title),
            'private': meta.private(),
            'comments': meta.comments(),
            'site_comments': self.site_config['presentation']['comments'],
            'category': category,
            'category_uri': self._make_root_uri(category,
                                                self.categories_dir),
            'date': meta.date(date_format),
            'datehtml': datehtml,
            'tags': meta.tag_list(),
            'content': content_html}

        # Publish original date if needed
        if meta.up_date():
            values['entry'].update({
                'up_date': meta.up_date(date_format),
                'up_datehtml': up_datehtml})

        outfile = self._make_output_file(
            title, self._entry_link_prefix(infile))
        return self._render_template('entry.html.j2', outfile, values)

    def gen_entries(self, date_format='%c'):
        """Generate all entries.

        :param date_format: Date format for entry
        :type date_format: str
        """
        for filename in os.listdir(self.entries_dir):
            if has_extension(filename, self.infile_ext):
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
            if has_extension(filename, self.infile_ext):
                inpath = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(inpath,
                                   self.site_config['wlocale']['encoding'],
                                   logger=self.logger).metadata())

                private = meta.private()
                title = meta.title()
                summary = meta.summary()
                category = meta.category(
                    self.site_config['presentation']['default_category'])
                category_uri = self._make_root_uri(category,
                                                   self.categories_dir)
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d %H:%M:%S')
                uri = self._make_entry_uri(title, filename, force_root=True)

                # Generate archive
                if not private:
                    total_entries += 1
                    val = {'title': title, 'summary': summary,
                           'date': date, 'date_idx': date_idx,
                           'uri': uri, 'category': category,
                           'category_uri': category_uri}
                    entries.append(val)

        # Sort chronologically descent
        entries = sorted(entries, key=lambda k: k['date_idx'],
                         reverse=True)

        total_pages = ceil(total_entries / max_entries_per_page)
        values = self.template_values.copy()

        # FIXME :: Merge this scenario with the following loop
        # Generate 'index.html' even when there are no posts
        if total_entries == 0:
            outfile = self._make_output_file()
            print(outfile)
            self._render_template('entries.html.j2', outfile, values)

        # Home page (and subsequent ones)
        for cur_page in range(1, total_pages + 1):
            min_page = (cur_page - 1) * max_entries_per_page
            max_page = cur_page * max_entries_per_page

            values['entries'] = entries[min_page:max_page]
            values['cur_page'], values['total_pages'] = \
                cur_page, total_pages

            if cur_page == 1:
                # the home page, the "index.html" of the site
                outfile = self._make_output_file()
            else:
                # subsequent pages other that the first
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
            if has_extension(filename, self.infile_ext):
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post,
                                   self.site_config['wlocale']['encoding'],
                                   logger=self.logger).metadata())

                private = meta.private()
                title = meta.title()
                #summary = meta.summary()
                category = meta.category(
                    self.site_config['presentation']['default_category'])
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d')
                uri = self._make_entry_uri(title, filename)

                # Generate archive
                if not private:
                    val = {'uri': uri, 'title': title, 'date': date,
                           'date_idx': date_idx, 'category': category}
                    d = datetime.strptime(meta.date('%Y-%m-%d'), '%Y-%m-%d')
                    idx_year = d.strftime('%Y')
                    # %m to sort chronologically
                    idx_month = d.strftime('<%m> %B')
                    if idx_year in archive:
                        if idx_month in archive[idx_year]:
                            archive[idx_year][idx_month].append(val)
                        else:
                            archive[idx_year][idx_month] = [val]
                        # sort entries
                        archive[idx_year][idx_month] = \
                            sorted(archive[idx_year][idx_month],
                                   key=lambda k: k['date_idx'],
                                   reverse=False)
                    else:
                        archive[idx_year] = dict()
                        archive[idx_year][idx_month] = [val]

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
            if has_extension(filename, self.infile_ext):
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post,
                                   self.site_config['wlocale']['encoding'],
                                   logger=self.logger).metadata())

                private = meta.private()
                title = meta.title()
                #summary = meta.summary()
                category = meta.category(
                    self.site_config['presentation']['default_category'])
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d')
                comments = meta.comments()
                uri = self._make_entry_uri(title, filename)

                # Generate archive
                if not private:
                    val = {'uri': uri, 'title': title, 'date': date,
                           'date_idx': date_idx, 'comments': comments}
                    if category in archive:
                        archive[category].append(val)
                    else:
                        archive[category] = [val]
                    # sort entries
                    archive[category] = sorted(archive[category],
                                               key=lambda k: k['date_idx'],
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
            if has_extension(filename, self.infile_ext):
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post,
                                   self.site_config['wlocale']['encoding'],
                                   logger=self.logger).metadata())

                private = meta.private()
                title = meta.title()
                #summary = meta.summary()
                category = meta.category(
                    self.site_config['presentation']['default_category'])
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d')
                uri = self._make_entry_uri(title, filename)

                # Generate archive
                if not private:
                    val = {'uri': uri, 'title': title, 'date': date,
                           'date_idx': date_idx}
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
                                       k['date_idx'], reverse=True)
            outfile = self._make_output_file(category, self.categories_dir)
            self._render_template('cat.html.j2', outfile, values)

    def gen_tags(self, date_format='%c'):
        """Generate tags pages.

        :param date_format: Date format for entry
        :type date_format: str
        """
        entries_by_tag = dict()
        for filename in os.listdir(self.entries_dir):
            if has_extension(filename, self.infile_ext):
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post,
                                   self.site_config['wlocale']['encoding'],
                                   logger=self.logger).metadata())

                private = meta.private()
                title = meta.title()
                #summary = meta.summary()
                category = meta.category(
                    self.site_config['presentation']['default_category'])
                tag_list = meta.tag_list()
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d')
                uri = self._make_entry_uri(title, filename)

                # Generate archive
                if not private:
                    val = {'uri': uri, 'title': title, 'date': date,
                           'date_idx': date_idx, 'category': category}
                    for tag in tag_list:
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
                                       k['date_idx'], reverse=True)
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
            if has_extension(filename, self.infile_ext):
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post,
                                   self.site_config['wlocale']['encoding'],
                                   logger=self.logger).metadata())
                private = meta.private()
                title = meta.title()
                tag_list = meta.tag_list()

                # Generate archive
                if not private:
                    val = {'title': title}
                    for tag in tag_list:
                        if tag in entries_by_tag:
                            entries_by_tag[tag].append(val)
                        else:
                            entries_by_tag[tag] = [val]

        # multipliers seq. for tag size in function of times repeated
        tagcloud_seq = [0, 14, 21, 27, 32, 38, 42, 45, 47, 48]

        # One page for each tag
        values = self.template_values.copy()
        values['tags'] = []
        for tag in entries_by_tag:
            if tag:
                tagname, tagfreq = tag, len(entries_by_tag[tag])
                mult = 100 + int(tagcloud_set.last
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

        .. note:: Since this add new data to the base template, it must
                  be invoked first, before generating any other page.
        """
        for filename in os.listdir(self.pages_dir):
            if has_extension(filename, self.infile_ext):
                inpath = os.path.join(self.pages_dir, filename)
                ml = Mulang(inpath,
                            self.site_config['wlocale']['encoding'],
                            logger=self.logger)
                meta = Meta(ml.metadata())

                if meta.navigation():
                    title = meta.title()
                    uri = self._make_root_uri(title)

                    values = self.template_values.copy()
                    values['page'] = {  # append
                        'title': title,
                        'raw_title': strip_html_tags(title),
                        'uri': uri}

                    # Update base template values to get pages links in
                    # nav. bar only if the page is set to be in the
                    # navigation bar
                    self.template_values['blog']['page_links'].append(
                        [values['page']['title'],
                         values['page']['uri']])

                    self.logger and self.logger.info(
                        'Added page to navigation: "%s"', inpath)

    def gen_page(self, infile):
        """Generate a HTML page from its Mardkdown counterpart.

        :param infile: Markdown file to parse
        :type infile: str
        :return: Generated HTML
        :rtype: str
        """
        inpath = os.path.join(self.pages_dir, infile)
        ml = Mulang(inpath, self.site_config['wlocale']['encoding'],
                    logger=self.logger)
        meta = Meta(ml.metadata())
        content_html = ml.html()

        title = meta.title()

        values = self.template_values.copy()
        values['page'] = {  # append
            'title': title,
            'raw_title': strip_html_tags(title),
            'content': content_html}

        outfile = self._make_output_file(title)
        return self._render_template('page.html.j2', outfile, values)

    def gen_pages(self):
        """Generate all pages."""
        for filename in os.listdir(self.pages_dir):
            if has_extension(filename, self.infile_ext):
                self.gen_page(filename)

    def gen_feed(self, feed_format="atom", outfile='feed.xml'):
        """Generate blog feed.

        :param feed_format: Feed format string ('rss' or 'atom').
                            If invalid value, will default to 'atom'
        :type feed_format: str
        :param outfile: Output filename
        :type outfile: str
        """
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
            if has_extension(filename, self.infile_ext):
                infile = os.path.join(self.entries_dir, filename)
                ml = Mulang(infile,
                            self.site_config['wlocale']['encoding'],
                            logger=self.logger)
                meta = Meta(ml.metadata())
                author = self.site_config['info']['site_name'] \
                    if not meta.author() \
                    else meta.author()
                email = self.site_config['info']['site_author_email'] \
                    if not meta.email() \
                    else meta.email()
                content_html = ml.html()
                private = meta.private()
                title = meta.title()
                summary = meta.summary()
                up_date_idx = meta.up_date('%Y-%m-%d %H:%M:%S')
                date_idx = meta.date('%Y-%m-%d %H:%M:%S')
                timezone = 'UTC' if not meta.date('%Z') else meta.date('%Z')
                date_iso8601 = meta.date('%Y-%m-%dT%H:%M') + timezone
                up_date_iso8601 = meta.up_date('%Y-%m-%dT%H:%M') \
                    + timezone if meta.up_date('%Y-%m-%dT%H:%M') \
                               else None
                pub_date = date_iso8601
                up_date = up_date_iso8601

                #updated = datetime.strptime(date_iso8601, '%Y-%m-%dT%H:%M%Z')
                uri = self._make_entry_uri(title, filename)
                full_uri = os.path.join(self.site_config['uri']['canonical'],
                                        self.site_config['uri']['base'], uri)

                if not private:
                    val = {'title': strip_html_tags(title),
                           'subtitle': summary,
                           'content_html': content_html,
                           'author': author,
                           'email': email,
                           'full_uri': full_uri,
                           'date_idx': date_idx,
                           'pub_date': pub_date,
                           'up_date': up_date}
                    entries.append(val)

        # sort chronologically descent
        entries = sorted(entries, key=lambda k: k['date_idx'],
                         reverse=True)
        for entry in entries:
            fnew = feed.add_entry()
            fnew.id(slugify(strip_html_tags(entry['title'])))
            fnew.title(entry['title'])
            fnew.description(entry['content_html'])
            if up_date:
                fnew.updated(entry['up_date'])
            fnew.pubDate(entry['pub_date'])
            # , 'email':entry['email']})
            fnew.author({'name': entry['author']})
            fnew.link(href=entry['full_uri'], rel='alternate')

        if feed_format == "rss":
            feed.rss_file(os.path.join(self.site_config['dirs']['deploy'],
                                       outfile))
        else:
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

        .. note:: The first thing that has to be generated is the
                  navigation links for all user defined pages.
                  Otherwise those links could be left behind on page
                  pages.
        """
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

