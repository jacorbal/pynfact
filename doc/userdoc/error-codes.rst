.. vim: set ft=rst fenc=utf-8 tw=72 nowrap:

***********
Error codes
***********

These error codes are referencing the exit status of the application
after an abnormal termination.  The error codes are divided in the
following categories:

#. Command line interface (``cli.main``)
#. Configuration problems (``Yamler``)
#. Markdown to HTML Parser (``Mulang``)
#. Builder (``Builder``)
#. File manager errors (``fileman.``)
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

Markdown to HTML parsing error codes (``3x``)
=============================================

There are no error codes for parsing operations, but this space is
reserved for that.

Builder error codes (``4x``)
============================

**ERROR 41**: *Unsupported locale setting*
    The builder is trying to generate the blog structure with a locale
    that is not configured in the system.  Check the configuration file,
    ``config.yml`` and check the locale settings.  Use only values that
    are installed on your system.

File manager error codes (``5x``)
=================================

There are no error codes for file operations, but this space is reserved
for that.

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

