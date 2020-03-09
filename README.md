PynFact
=======

  * **Description:** A blog-oriented static website generator.
  * **Current version:** 0.4.0 (2020-03-10)

![PynFact Logo][pynfact_logo]

Features
--------

  * Input format: Markdown
  * Output format: HTML&nbsp;5
  * Jinja2 templates
  * Locale support (`gettext`)


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

In the future, this process will be more automatic and simpler:

  1. Go to the downloaded source, and then to the `pynfact` directory
  2. Type: `$ python3 pynfact init myblog` (or any name you want for your blog)
  3. Copy the binaries into the blog: `$ cp -r pynfact myblog`
  4. Go to your blog and test: `cd myblog; make test`
  5. Test in any browser: `localhost:4000`

You can specify any port in the `Makefile`, and you can move the folder
`myblog` to any place in your system.


Recent changes
--------------

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
taken. `:(`


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

