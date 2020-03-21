##########
To-Do List
##########

.. rubric:: TO-DO LIST

**The number in brackets represents the priority
(0:none; 5:urgent; X:done)**

Coding style
============

* **[3]** In *all*, use a **much more** *pythonic* code
* **[4]** Refactor ``Builder`` class in simpler methods (if possible)
* **[X]** Refactor ``Meta`` class in simpler methods
* **[X]** Get array of meta data, instead of individual attributes
* **[X]** Use ``argparse`` in ``cli.py``
* **[2]** Single-sourcing_ the package version in an efficient way

Unit testing
============

* **[4]** Finish beta tests stage 2 and upload them to repository

Next features for future versions
=================================

Content configuration
---------------------

* **[X]** Pages allowed to be ``private``
* **[3]** Tags (and categories) in bold and/or italics (accept MU lang)
* **[X]** Slug in pages taken from title, not from filename

Internal references
-------------------

References inter-posts or inter-pages are required, imitating the Wiki
syntax.  This syntax will be the same for Markdown and reStructuredText
documents, so it has to be in a way that do not interfere with their
natural syntax.

Proposals:

#. Using double brackets: ``[[ ... ]]``
#. Using double curly braces: ``{{ ... }}``

The second syntax is very reminiscent of Jinja2 templates, and event the
content documents will not interfere with the source templates, it could
be confusing.  It'll be better to use the brackets.

#. **[5]** Internal links between posts and pages in markdown content:

   * ``This [[ linkpost "Title of the post" ]]``, or
   * ``This [[ linkpost slug-of-the-post ]]``, or
   * ``This [[ linkpost filename-of-post.md ]]``;

   * ``This [[ linkpage "Title of the page" ]]``, or
   * ``This [[ linkpage slug-of-the-page ]]``, or
   * ``This [[ linkpage filename-of-page.md ]]``.

#. **[5]** Internal links between tags and categories:

   * ``This [[ linkcat "Category name" ]]``, or
   * ``This [[ linkcat cateogry-slug ]]``, or

   * ``This [[ linktag "Tag name" ]]``, or
   * ``This [[ linktag tag-slug ]]`` .

#. **[5]** Include source from other files:

   * ``[[ source media/files/lipsum.txt ]]``, or
   * ``[[ source media/files/data.c ]]``.

In case of malformed "Wiki" links, it'll be considered as a comment and
removed from final HTML5 content, therefore, not parsed.

Exceptions
~~~~~~~~~~

Parsing errors are code ``3x``:

* Error **35**: Double brackets are opened, but not properly closed

* Error **36**: The instruction within is malformed

* Error **37**: The page/post/category/tag does not exist

Locale
------

* **[3]** Language meta tag for pages and posts, and taken by the
  template to change the language of the section.

  * ``entry.html.j2``:
    ``<article class="entry" lang="{{ base.lang }}"> [...]``

  * ``page.html.j2``:
    ``<article class="page" lang="{{ base.lang }}"> [...]``

The value ``language`` from ``config.yaml`` sets the ``<body>`` element,
the ``language`` sets the ``<article>`` element if defined.

Feed
----

* **[X]** Accept a new value from the ``config.yaml`` file.  Currently
  is set to accept either ``rss`` or ``atom``, but not to disable it.
  Any value for this key that is not one of ``{'rss', 'atom'}`` will
  disable the feed.

Meta information
----------------

* **[5]** Author[s] taken as list, there could be more than one
* **[1]** Author[s] meta tag for pages
  In the end, why?  The only reason would be to show the page author as
  the page metadata, below the title.

* **[4]** Show author in posts

  * Always?, or
  * only when there are more than one author?, or
  * depending on value in ``config.yaml``?

* **[5]** Allow user to define own slug instead of autogenerating it
* **[0]** Allow insert date in current locale (not worth it)

Input format
------------

* **[X]** Add reStructuredText as input format (``docutils``).
  Identify the document by the extension, depending on which, the
  interpreter parses Markdown or reStructuredText (HTML5 only)

Functionality
-------------

* **[X]** Logging, instead of using ``stdout`` when generating the site
* **[2]** User should choose where to store the logs in ``config.yaml``.

* **[X]** Logging output configured by ``argparse``:

  * ``pynfact --log=/dev/stdout``
  * ``pynfact --log=~/pynfact.log``

* **[2]** User should choose the deploy directory name in ``config.yaml``
* **[2]** Bugs report: allow the user to file a bug

Customization
-------------

* **[1]** Add themes (template changing system):

  * ``pynfact --loadtheme <theme1>``: replace user templates with new theme
  * ``pynfact --savetheme <mytheme>``: save as ``mytheme`` in folder ``themes``

Intentions
==========

Things that will change for sure.

Intended command line interface
-------------------------------

* **[5]** Check if CWD is a pynfact blog one when invoking ``--init``
* **[1]** Logs in specific directory: ``log/`` (?)
* **[3]** Do not write a log file on ``--init`` operations, only
  ``--build`` and ``--serve`` because those require to be within the
  blog directory, so there will be no logs outside the related path.

Command line options:

* **[X]** Initialize: ``pynfact -i [name]``  or ``pynfact --init[=name]``
* **[X]** Serve: ``pynfact -s`` or ``pynfact --serve``
* **[X]** Set port:  ``pynfact -p 4002`` or ``pynfact --port=4002``
* **[X]** Build: ``pynfact -b`` or ``pynfact --build``
* **[X]** Logging: ``pynfact -l file`` or ``pynfact --log=file``
* **[ ]** Configuration: ``pynfact -c myconfig.yaml`` or ``--config=``
* **[ ]** Deploy dir: ``pynfact -d _deploy`` or ``pynfact --deploy-dir=_dpl``
* **[ ]** Theme load: ``pynfact -L theme`` or ``pynfact --loadtheme=theme``
* **[ ]** Theme save: ``pynfact -S theme`` or ``pynfact --savetheme=theme``

Templates
=========

* **[1]** ``base.html.j2`` should not have there those four Jinja2 lines
  since that's the file the user will be dealing with (?)


.. _Single-sourcing:
    https://packaging.python.org/guides/single-sourcing-package-version/

