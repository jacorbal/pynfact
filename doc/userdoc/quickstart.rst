.. vim: set ft=rst fenc=utf-8 tw=72 nowrap:

**********
Quickstart
**********

It is recommended to read all documentation files, or to ask questions
via the typical communication methods, but, for the impatient ones, here
are the summary instructions to get your static blog generated.

Installation
============

PynFact requires Python 3.5+.  You may install it by running the
following command in any terminal::

    pip install pynfact

In some systems where Python 2 is the default version, it's possible
that the installer for Python 3 is called ``pip3``.

Either way, you may run ``pip`` by invoking ``python`` directly::

    python3 -m pip install pynfact

This will install ``pynfact`` to your local system.  In case of wanting
``pynfact`` available to all users, run the command as ``root`` or use
``sudo``::

    sudo pip install pynfact

Starting a new blog
===================

Choose name for your static weblog, for the sake of this examples, it'll
be used ``myblog``.  Run ``pynfact`` initializer by typing::

    pynfact init myblog

A new folder named ``myblog`` will be created with the basic structure for
the website.  Switch to it::

    cd myblog

Testing the site
================

There's a dummy article with title "First Entry" in the folder
``posts``.  Right now, it's the only posts.

To generate the site, run::

    pynfact build

Every article and page will be parsed, in this case, only the post
``first_entry.md``.  A new folder named ``_build`` is created containing
the deployed static code.

In order to preview the website::

    pynfact serve

And use any browser at `<http://localhost:4000/>`_

Send and keyboard interrupt (``^C``) to the terminal to finish the
preview.

If the site works, congratulations!, you may put aside the
``first_entry.md`` post in the ``posts`` directory.  It's possible to
delete it, but also recommended to keep it as a template.  Just change
the extension to something that is not ``.md`` so it won't be generated
in future builds.

+----------------------------------------------------------------------+
| **NOTE.**  The command line interface will change in future versions |
| by the use of ``argparse``.                                          |
+----------------------------------------------------------------------+

