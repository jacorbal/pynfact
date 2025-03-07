.. vim: set ft=rst fenc=utf-8 tw=72 nowrap:

***********
Error codes
***********

These error codes are referencing the exit status of the application
after an abnormal termination.  The error codes are divided in the
following categories:

#. Command line interface (``main``)
#. Configuration problems (``Yamler``)
#. Markup language to HTML Parser (``Parser``)
#. Builder (``Builder``)
#. File manager errors (``fileman``)
#. Server (``Server``)

An exit code equal to ``0`` means *Success!*

Here's a description of each error, and the most likely solution:

CLI error codes (``1x``)
========================

**ERROR 11**: *Unable to initialize the website structure*
    It's not possible to create directories and files in the directory
    where the initializer has been invoked.  Check the permissions of
    the current working directory, and the user and group .

Configuration error codes (``2x``)
==================================

**ERROR 21**: *Cannot read the configuration file*
    The configuration file named ``config.yml`` cannot be found.  Try
    initializing another blog in a different folder and copy the
    configuration file into the directory of your blog.

**ERROR 22**: *Key not found in configuration file*
    The configuration parser is trying to access to a key identifier
    that does not exist in the configuration but is needed to build the
    site.  Check the configuration file keys and compare them to those
    in the documentation.

Markup language to HTML parsing error codes (``3x``)
====================================================

**ERROR 31**: *Missing or malformed title key in "{filename}" metadata*
    The content of *{filename}* doesn't have a "title" meta tag, or it
    is malformed.  The title is required in every post or page.

**ERROR 32**: *Missing or malformed date key in "{filename}" metadata*
    The content of *{filename}* doesn't have a "date" meta tag, or it
    is malformed.  Dates are required in posts, but not in pages.

A malformed meta tag is written using diacritics or invalid characters,
or has a value that spans across multiple lines.

Key identifiers only accept characters in range ``[A-Za-z0-9]``.  Also,
if the value of the meta tag is a very long string written in multiple
lines, all subsequent lines must be indented at least four characters.

**ERROR 33**: *Empty title value in "{filename}" metadata*
    The metadata tag for title exists, but it's empty.  This tag is
    mandatory for posts and pages and cannot be empty.

**ERROR 34**: *Empty or invalid date value in "{filename}" metadata*
    The metadata tag for date exists, but it's empty or is not a date.
    This tag is mandatory for posts and cannot be empty.

Builder error codes (``4x``)
============================

**ERROR 41**: *Unsupported locale setting*
    The builder is trying to generate the blog structure with a locale
    that is not configured in the system.  Check the configuration file,
    ``config.yml`` and check the locale settings.  Use only values that
    are installed on your system.

File manager error codes (``5x``)
=================================

There are no error codes for file operations yet..., but this space is
reserved for that.

Server error codes (``6x``)
===========================

**ERROR 61**: *Deploy directory not found*
    The site has not being generated yet, so there's no deploy folder,
    typically ``_build``.  Try to rebuild the static site by running
    ``pynfact --build`` before trying to serve again.

**ERROR 62**: *Address not valid or already in use*
    The address and port trying to be used, by default
    `<http://localhost:4000>`_, is being used by another process.  Try
    closing that process, or specify another port by using the command
    line options.
