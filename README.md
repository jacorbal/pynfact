PynFact
=======

  * **Description:** A blog-oriented static website generator
  * **Current version:** 1.0.2.dev4 (2020-03-12)

Pynfact is a simple static website generator oriented to chronological
content, like blogs or websites with historic and sequential data.  It
allows integration with external scripts, comment engines such as
Disqus, TalkYard, etc., or Google Analytics...  Theming and
configuration is possible by editing Jinja2 templates.

![PynFact Logo][pynfact_logo]


Features
--------

  * Input format: Markdown
  * Output format: HTML&nbsp;5
  * Configuration: Jinja2 templates
  * Locale support (`gettext`)
  * Code syntax highlighting (`Pygments`)
  * Atom/RSS feed generation


Requirements
------------

  * **Python 3**
  * **Markdown**: Python implementation of Markdown
  * **Unidecode**: ASCII transliterations of Unicode text
  * **feedgen**: Feed Generator (Atom, RSS, Podcasts)
  * **Jinja2**: A small but fast and easy to use stand-alone template
   engine written in pure Python


Installation
------------

Run:

    $ pip install pynfact

(If your default version of Python is 2.x, maybe you need to type `pip3`
instead of `pip`)


Usage
-----

The interaction is done by command line.  Only a few commands are
needed:

  1. `pynfact init <myblog>`: Create a folder with all needed content
  2. Go to that directory: `cd <myblog>`
  3. Configure settings in `config.yml`, title, name, language...
  4. `pynfact build`: Generates the static content
  5. `pynfact serve`: Serves locally to test the results
   (by default at `localhost:4000`)

More details at: <https://github.com/jacorbal/pynfact/wiki> (soon).


Recent changes
--------------

  * Deployed as Python package at PyPI: <https://pypi.org/project/pynfact/>
  * Added Esperanto locale (`eo`)
  * Builder class constructor simplified, now takes a configuration
   dictionary, sorted semantically
  * Using `feedgen` instead of `pyatom` to generate RSS/Atom syndication
   feeds


Why this name?
--------------

Granted it will be used on the "web", the word "log" in Latin may be
translated as *INdicem FACTorum*, hence *InFact* or **-nFact** to be
more easily pronounceable when prepending the prefix *py-*, an indicator
of the programming language where it has been developed.

Also, *pyblog*, *pyblic*, *pyweblog* and many other cool names were
already taken.


Bugs
----

Lots!  This project is still in development, so there are probably a
lot of bugs that need to be fixed before is deployed as a package.


License
-------

*PynFact* is distributed under the MIT license.
More information in `LICENSE` file.

(c) 2012-2020, J. A. Corbal.


[pynfact_logo]: logo.png

