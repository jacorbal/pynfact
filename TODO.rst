##########
To-Do List
##########

.. rubric:: TO-DO LIST

The number in brackets represents the priority (0:none, 5:urgent)

Code
====

* **[3]** Break ``Builder`` into more classes and functions, redundant code!

* **[1]** In ``struri.py``:

  * Apply ``re.sub`` to all members of the list

* **[1]** In ``mulang.py``:

  * Retrieve metainfo without regenerating all HTML from Markdown

* **[3]** In *all* of the above and the rest:

  * Use a much more *pythonic* code

* **[2]** Single-sourcing_ the package version in an efficient way

* **[4]** Use ``argparse`` in ``cli.py``

Next features
=============

Structure
---------

* **[5]** Pages allowed to be ``private``
* **[5]** Slug in pages taken from title, not from filename
* **[3]** Tags (and categories) in bold and/or italics (accept MU lang)

Internal references
-------------------

* **[5]** Internal links between posts and pages in markdown content:

  * ``This [link]({{ link posts/post_filename.md }})`` or
  * ``This [link]({{ link posts/post_filename }})``;
  * ``This [link]({{ link page/page_filename }})``,
    (with or without extension?).

* **[5]** Internal links between tags and categories:

  * ``This [link]({{ link tag/tag_slug }})``;
  * ``This [link]({{ link cat/cat_slug }})``;

* **[5]** Include source from other files:

  * ``{{ source media/files/lipsum.txt }}``
  * ``{{ source media/files/data.c }}``

Locale
------

* **[3]** Language meta tag for pages and posts, and taken by the
  template to change the language of the section.

  * ``entry.html.j2``:
    ``<article class="entry" lang="{{ base.lang }}"> [...]``

  * ``page.html.j2``:
    ``<article class="page" lang="{{ base.lang }}"> [...]``

Meta information
----------------

* **[5]** Author[s] taken as list, there could be more than one
* **[1]** Author[s] meta tag for pages
* **[5]** Insert date in current locale
* **[5]** Allow user to define own slug instead of autogenerating it

Input text
----------

* **[1]** Add reStructuredText as input format, bedides Markdown
  Requires a new entry in ``config.yml``: ``input_format=["md"|"rst"]``,
  **OR**, maybe, identify the document by the extension, depending on
  which, theinterpreter parses Markdown or reStructuredText.

Functionality
-------------

* **[3]** Logging, instead of using ``stdout`` when generating the site,
  available by the user in ``blog/logs/`` folder

  * ``pynfact --log=stdout``
  * ``pynfact --log=~/pynfact.log``

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

* Initialize a site: ``pynfact -i [name]``  or ``pynfact --init[=name]``
* Serve: ``pynfact -s`` or ``pynfact --serve``
* Set port:  ``pynfact -p 4002`` or ``pynfact --port=4002``
* Build: ``pynfact -b`` or ``pynfact --build``
* Deploy dir: ``pynfact -d _deploy`` or ``pynfact --deploy-dir=_deploy``
* Theme load: ``pynfact -L theme`` or ``pynfact --loadtheme=theme``
* Theme save: ``pynfact -S theme`` or ``pynfact --savetheme=theme``
* Logging: ``pynfact -w file`` or ``pynfact --write-log=file``

Intended userspace
------------------

::

    my-pynfact-blog/
        config.yml
        logs/
        pages/*.md
        posts/*.md
        static/
            css/
        templates/*.j2
        themes/
            theme1/*j2
            theme2/*j2
            <[...]>

Templates
=========

* **[1]** ``base.html.j2`` should not have there those four Jinja2 lines
  since that's the file the user will be dealing with (?)


.. _Single-sourcing:
    https://packaging.python.org/guides/single-sourcing-package-version/

