#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Main entry point.

:copyright: © 2012-2020, J. A. Corbal
:license: MIT
"""
from pynfact.cli import arg_build
from pynfact.cli import arg_init
from pynfact.cli import arg_serve
from pynfact.cli import set_logger
import argparse
import sys


try:
    import colored_traceback.auto
    colored_traceback.add_hook(always=True)
except ImportError:
    pass


def main():
    """Manage the command line arguments.

    .. versionchanged:: 1.2.0a1
        Implement ``logging`` instead of printing to ``stdout`` and/or
        ``stderr``.

    .. versionchanged:: 1.3.1a1
        Retrieve arguments by using :mod:`argparse`.

    .. versionchanged:: 1.3.1a2
        Move functions to :mod:`cli` and renamed file as ``main.py``.
    """
    parser = argparse.ArgumentParser(description=
                "PynFact!:"
                " A static blog generator from Markdown to HTML5",
            prog="pynfact",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rgroup = parser.add_mutually_exclusive_group(required=True)

    rgroup.add_argument('-i', '--init', default=None,
                        metavar='<blog>',
                        help="initialize a new blog structure")
    rgroup.add_argument('-b', '--build', action='store_true',
                        help="parse input files and build the website")
    rgroup.add_argument('-s', '--serve', default='localhost',
                        const='localhost',
                        metavar='<host>', nargs='?',
                        help="set host where to serve the blog")
    parser.add_argument('-p', '--port', default=4000,
                        metavar='<port>', type=int,
                        help="set port to listen to when serving")
    parser.add_argument('-l', '--log', default='pynfact.err',
                        metavar='<logfile>',
                        help="set a new error log filename or 'none'")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase output verbosity")

    # Print help if no arguments supplied
    args = parser.parse_args(None if sys.argv[1:] else ['--help'])

    # Process arguments
    logger = set_logger(args.verbose, error_log=args.log)
    if args.init:
        arg_init(logger, args.init)
    elif args.build:
        arg_build(logger, default_content_ext='.md')
    elif args.serve:
        arg_serve(logger, args.serve, int(args.port))


# Main entry
if __name__ == '__main__':
    main()

