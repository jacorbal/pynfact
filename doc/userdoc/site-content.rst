.. vim: set ft=rst fenc=utf-8 tw=72 nowrap:

************
Site content
************

Articles
========

All articles are in the directory ``posts``.  Everything with the
a valid extension in ``posts/*`` will be parsed; everything else will be
ignored.

By default, there is a dummy first entry as a test called
``first_entry.md``.  It may serve as a template for future posts, but
when you have your PynFact site working, you may want to rename to a
different extension, so it will be ignored, and therefore, not parsed,
in future builds.

Pages
=====

Pages are stored in the directory ``pages``, and also must have a valid
extension in order to be recognized by the parser.  Everything with the
valid extension will be parsed; everything else will be ignored.  The
syntax is identical to the one of articles.  A link to a page will
appear in the navigation bar by default, unless that feature is
deactivated for that particular page.

Format
======

Markdown and reStructuredText
-----------------------------

Pages and articles use the same format, a markdown file with extension
``.md``, ``.mdown``, ``.mkdown``, or ``.markdown``, and a heading
containing meta information.  An example of post could be::

    Title: Post title
    Summary: A _small_ summary for this *PynFact* entry. This summary
             is way two lines long, but it doesn't matter.
    Category: Miscellaneous
    Tags: tag1, tagtwo, tag three, Four
    Date: 2020-03-11 11:11 PM


    Here begins the *post*, in Markdown until the end of the file.
    Since the level-1 header `h1` is reserved for the title, all
    subsequent headers should begin in the second level.

.. note::
    When a string is too long that requires more than one line, all the
    lines from the second one 'til the end  must be indented at least
    four spaces.

And for a page::

    Title: Page title


    Here begins the *page*, in Markdown until the end of the file.
    Since the level-1 header `h1` is reserved for the title, all
    subsequent headers should begin in the second level.


In reStructuredText is very similar.  The accepted extensions are
``.rst``, ``.rest``, and ``.rtext``  The examples above, in
reStructuredText can be written as::

    :Title: Post title
    :Summary: A _small_ summary for this *PynFact* entry. This summary
        is way two lines long, but it doesn't matter.
    :Category: Miscellaneous
    :Tags: tag1, tagtwo, tag three, Four
    :Date: 2020-03-11 11:11 PM


    Here begins the *post*, in Markdown until the end of the file.
    Since the level-1 header `h1` is reserved for the title, all
    subsequent headers should begin in the second level.

or, not using the title as a metadata tag, and include it as part of the
reStructuredText syntax::

    Post title
    ==========

    :Summary: A _small_ summary for this *PynFact* entry. This summary
        is way two lines long, but it doesn't matter.
    :Category: Miscellaneous
    :Tags: tag1, tagtwo, tag three, Four
    :Date: 2020-03-11 11:11 PM


    Here begins the *post*, in Markdown until the end of the file.
    Since the level-1 header `h1` is reserved for the title, all
    subsequent headers should begin in the second level.


In case of not wanting a link to a page in the navigation bar, add the
meta tag ``Nav: no``, or ``Navigation: no``.  In Markdown::

    Title: Page title
    Navigation: no


    Here begins the *post*, in Markdown until the end of the file.
    This page **will not** appear in the navigation bar.


In reStructuredText::

    Page title
    ==========

    :Navigation: no


    Here begins the *post*, in Markdown until the end of the file.
    This page **will not** appear in the navigation bar.

Remeber that all metainformation tags are case insensitive.
Refer to :ref:`document-syntax` to learn more about the document format
for pages and articles.

Other static resources
======================

In the configuration file ``config.yml``, there's a variable called
``extra_dirs``.  There you may specify which directories will be copied
to the built static site.  By default is set to ``media``::

    extra_dirs = ['media']

If the directory does not exist, it will be ignored.  If exists, it will
be copied to the ``_build`` folder.

It's possible to include more directories, separated by commas::

    extra_dirs = ['pdfs', 'images', 'data']

But its also a good practice to keep a low number of directories.  It's
encouraged to keep only one directory named ``media``, and create a
sub-tree within it, for example::

    media/
    ├── data/
    │   ├── essays.tar.gz
    │   └── mybooks.txt
    ├── images/
    │   └── logo.png
    └── pdfs/
        ├── document1.pdf
        └── document2.pdf

