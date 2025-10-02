.. vim: set ft=rst fenc=utf-8 tw=72 nowrap:

*******************
Install and upgrade
*******************

Installing
==========

Using ``pip`` or ``pipx``
-------------------------

Both ``pip`` and ``pipx`` are package management tools for Python, but
they serve different purposes.  ``pip`` is primarily used to install and
manage Python packages from the Python Package Index (PyPI) and installs
packages into the current Python environment, which can sometimes lead
to dependency conflicts.  On the other hand, ``pipx`` is designed for
installing and running standalone Python applications in isolated
environments.  This means that each application gets its own set of
dependencies, preventing version clashes and making it easier to manage
command-line tools that are built in Python.

PynFact requires Python 3.6+.  You may install it by running the
following command in any terminal::

    pip3 install pynfact

In some systems where Python 2 is the default version, it's possible
that the installed for Python 3 is called ``pip3``.  Either way, you may
run ``pip`` by invoking ``python`` directly, after activating your
virtual environment::

    python3 -m pip3 install pynfact

This will install ``pynfact`` to your local system.  In case of wanting
``pynfact`` system-wide, i.e., available to all users, run the command as
``root`` or use ``sudo``::

    sudo pip3 install pynfact

Or, alternatively, using ``pipx`` (**recommended**)::

    pipx install pynfact

Downloading the source
----------------------

Pynfact require some dependencies in order to work, so make sure that
the following packages are on your system:

* ``docutils``: Python Documentation Utilities
* ``feedgen``: Feed Generator (Atom, RSS, Podcasts)
* ``Jinja2`` : A small but fast and easy to use stand-alone template
  engine written in pure Python
* ``markdown``: Python implementation of Markdown
* ``python-dateutil``: Extensions to the standard Python ``datetime`` module
* ``unidecode``: ASCII transliterations of Unicode text

Download the project source, either from `GitHub`_ or from `PyPI`_.
Once you have uncompressed the tarball, you may run::

    python3 setup.py install

Upgrading
=========

Using ``pip`` or ``pipx``
-------------------------

If you have installed PynFact by using ``pip`` and want to upgrade to
the latest stable release, you may do it by using the option
``--upgrade`` in the ``pip`` command (after setting your ``venv``)::

    pip3 install --upgrade pynfact

Or, with ``pipx`` (**recomended**)::

    pipx upgrade pynfact


Directly by source
------------------

In case of having used the source tarball, just repeat the installation
process with the latest stable version.


.. _GitHub: https://github.com/jacorbal/pynfact
.. _PyPI: https://pypi.org/project/pynfact/#files
