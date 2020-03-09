Py'nFact
========

  * **Description:** A blog-oriented static website generator.
  * **Current version:** 0.3.4 (2020-03-09)

![Py'nFact Logo][pynfact_logo]

Features
--------

  * Input format: Markdown
  * Output format: HTML 5
  * Jinja2 templates
  * Locale support (`gettext`)


Requirements
------------

  * **Python 3**
  * **Markdown**: Python implementation of Markdown
  * **Unidecode**: ASCII transliterations of Unicode text
  * **feedgen**: Feed Generator (ATOM, RSS, Podcasts)
  * **Jinja2**: A small but fast and easy to use stand-alone template
   engine written in pure Python


Installation
------------

  1. Go to the downloaded source, and then to the `pynfact` directory
  2. Type: `$ python3 pynfact init myblog` (or any name you want for your blog)
  3. Copy the binaries into the blog: `$ cp -r pynfact myblog`
  4. Go to your blog and test: `cd myblog; make test`
  5. Check in any browser: `localhost:4000`

You can specify any port in the `Makefile`, and you can move the folder
`myblog` to any place in your system.

In the future the process will be more automatic.

Why this name?
--------------

Granted it will be used on the "web", the word "log" in Latin may be
translated as *INdicem FACTorum*, hence *InFact* or **'nFact** to be
more easily pronounceable when prepending the prefix *py-*.

Also, *pyblog*, *pyblic*, *pyweblog* and many other cool names were
taken either in GitHub or Google Code.


Notes
-----

This project is in development, so there are some bugs that need to be
fixed and it needs to be deployed as a package.


License
-------

*Py'nFact* is distributed under the MIT license.
More information in `LICENSE` file.

(c) 2012-2020, J. A. Corbal.


[pynfact_logo]: logo.png

