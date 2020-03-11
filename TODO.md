TODO LIST
=========

Code
----

  * Break `Builder` into more classes and functions, redundant code!

  * In `struri.py`:
    * Apply `re.sub` to all members of the list

  * In `mulang.py`:
    * Retrieve metainfo without regenerating all HTML from Markdown

  * In *all* of the above and the rest:
    * Use a much more *pythonic* code

  * Single-sourcing the package version in an efficient way:
    <https://packaging.python.org/guides/single-sourcing-package-version/>

  * Deploy as package


Future fetures
--------------

  * Logging, instead of using `stdout` when generating the static site,
    available by the user in `blog/logs/` folder

  * Add themes (template changing system):
    * `pynfact loadtheme <theme-1>`: replace user templates with new theme
    * `pynfact savetheme <mytheme>`: save as `mytheme` in folder `themes`


  * Intended userspace:

        myblog/
            logs/
            posts/
                [...].md
            static/
                css/
            templates/
            themes/
                theme-1/
                theme-2/
                [...]
            aboud.md
            [...].md
            config.yml

Templates
---------

  * `base.html.j2` should not have there those four Jinja2 lines since
    that's the file the user will be dealing with (?)

