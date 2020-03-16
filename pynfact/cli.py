#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
Command line interface.

    :copyright: © 2012-2020, J. A. Corbal
    :license: MIT
"""
from pynfact.builder import Builder
from pynfact.server import Server
from pynfact.yamler import Yamler
import argparse
import logging
import os
import shutil
import sys


try:
    import colored_traceback.auto
    colored_traceback.add_hook(always=True)
except ImportError:
    pass


def set_logger(verbosity=False, error_log='pynfact.err',
               echo_log=sys.stdout):
    """Set up the system logger.

    :param verbosity: Show basic information, or also debug messages
    :type verbosity: bool
    :param error_log: Filename for the warnings and errors log
    :type error_log: str
    :param echo_log: Stream to write the default information log
    :type echo_log: _io.TextIOWrapper

    This function starts two logs, one stream on the standard output
    (``echo_log``) where the ``verbosity`` parameter can increase the
    volume of messages; and the error log (``error_log``), saved to a
    file but only logging errors and critical errors.  Warnings, errors
    and critical errors are displayed automatically to the standard
    output.

    The parameter ``verbosity`` concerns only to what is being displayed
    on screen concordingly with the log leves of the ``logging`` module.
    These levels may be specified by an integer value or by name.  These
    are their values:

    * 10: ``logging.DEBUG``
    * 20: ``logging.INFO``
    * 30: ``logging.WARNING``
    * 40: ``logging.ERROR``
    * 50: ``logging.CRITICAL``

    The following table illustrates what is getting logged:

    +---------------+--------------+--------------+---------------+
    | ``logging.``  | ``!verbose`` |  ``verbose`` | ``error_log`` |
    +===============+==============+==============+===============+
    | ``.DEBUG``    |              |      X       |               |
    +---------------+--------------+--------------+---------------+
    | ``.INFO``     |      X       |      X       |               |
    +---------------+--------------+--------------+---------------+
    | ``.WARNING``  |      X       |      X       |               |
    +---------------+--------------+--------------+---------------+
    | ``.ERROR``    |      X       |      X       |       X       |
    +---------------+--------------+--------------+---------------+
    | ``.CRITICAL`` |      X       |      X       |       X       |
    +---------------+--------------+--------------+---------------+
    | write log to: |  ``stdout``  |  ``stdout``  |   ``file``    |
    +---------------+--------------+--------------+---------------+

    The only way to deactivate the ``error_log`` is to use the command
    line option ``-l none``, or ``--log=none``.  Either way, the
    warnings, errors and critical messages will still be shown on
    screen, for any value of ``verbosity``.  What ``verbosity`` does is
    to enable or disabe the debug messages.
    """
    log_level = logging.DEBUG if verbosity else logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Default ``stdout`` handler, set by ``verbosity`` value
    echo_shandler = logging.StreamHandler(echo_log)
    echo_shandler.setLevel(log_level)
    echo_shandler.setFormatter(logging.Formatter(
        '[%(levelname)s]: %(message)s'))
    logger.addHandler(echo_shandler)

    # Errors and Critical errors handler (write to file)
    if error_log.lower() != 'none':
        warning_fhandler = logging.FileHandler(error_log)
        warning_fhandler.setLevel(logging.ERROR)
        warning_fhandler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s]: %(message)s'))
        logger.addHandler(warning_fhandler)

    return logger


def retrieve_config(config_file, logger=None):
    """Retrieve configuration from YAML file.

    :param config_file: YAML configuration filename
    :type config_file: str
    :param logger: Logger to pass it to the ``Yamler`` constructor
    :type logger: logging.Logger
    :return: Dictionary of configuration
    :rtype: dict
    """
    config = Yamler(config_file, logger)

    site_config = {
        'uri': {
            'base': config.retrieve('base_uri', '').strip('/'),
            'canonical': config.retrieve('canonical_uri', '').rstrip('/'),
        },
        'wlocale': {
            'encoding': config.retrieve('encoding', 'utf-8'),
            'locale': config.retrieve('locale', 'en_US.UTF-8'),
            'language': config.retrieve('site_language', 'en'),
        },
        'date_format': {
            'entry': config.retrieve('datefmt_entry', "%c"),
            'home': config.retrieve('datefmt_home', "%b %_d, %Y"),
            'list': config.retrieve('datefmt_list', "%Y-%m-%d"),
        },
        'info': {
            'copyright': config.retrieve('site_copyright'),
            'site_author': config.retrieve('site_author', "Nameless"),
            'site_author_email': config.retrieve('site_author_email', ''),
            'site_description': config.retrieve('site_description'),
            'site_name': config.retrieve('site_name', "My Blog"),
        },
        'presentation': {
            'comments': config.retrieve('comments').lower() == "yes",
            'default_category':
                config.retrieve('default_category', "Miscellaneous"),
            'feed_format': config.retrieve('feed_format', "atom"),
            'max_entries': config.retrieve('max_entries', 10),
        },
        'dirs': {
            'deploy': "_build",
            'extra': config.retrieve('extra_dirs')
        }
    }

    return site_config


def arg_init(logger, dst):
    """Initialize a new website structure.

    :param dst: Name of the folder containing the new website
    :type dst: str
    :param logger: Logger to pass it to the ``Yamler`` constructor
    :type logger: logging.Logger
    :raise: OSError
    """
    real_path = os.path.dirname(os.path.realpath(__file__))
    src = os.path.join(real_path, 'initnew')
    dst = dst

    # create new blog structure with the default values
    try:
        shutil.copytree(src, dst)
    except OSError:
        logger and logger.error(
            "Unable to initialize the website structure")
        sys.exit(11)


def arg_build(logger, default_content_ext='.md',
              config_file='config.yml'):
    """Build the static website after getting the site configuration.

    :param logger: Logger to pass it to the ``Builder`` constructor
    :type logger: logging.Logger
    """
    site_config = retrieve_config(config_file, logger)

    # Prepare builder
    template_values = {
        'blog': {
            'author': site_config['info']['site_author'],
            'base_uri': site_config['uri']['base'],
            'encoding': site_config['wlocale']['encoding'],
            'feed_format': site_config['presentation']['feed_format'],
            'lang': site_config['wlocale']['language'],
            'site_name': site_config['info']['site_name'],
            'page_links': [],
        }
    }

    # Build
    b = Builder(site_config, template_values,
                infile_ext=default_content_ext, logger=logger)
    b.gen_site()


def arg_serve(logger, host='localhost', port=4000):
    """Initialize the server to listen until keyboard interruption.

    :param logger: Logger to pass it to the ``Server`` constructor
    :type logger: logging.Logger
    """
    server = Server(host, port=port, path='_build', logger=logger)
    server.serve()


def main():
    """Manage the command line arguments."""
    parser = argparse.ArgumentParser(description="PynFact!:"
                                     " A static blog generator from"
                                     " Markdown to HTML5 with Jinja2")
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-i', '--init', default=None,
                       help="initialize a new blog structure")
    group.add_argument('-b', '--build', action='store_true',
                       help="build the website")
    group.add_argument('-s', '--serve', default='localhost',
                       help="set address to serve locally the blog")
    parser.add_argument('-p', '--port', default='4000', type=int,
                        help="set port to listen to when serving")
    parser.add_argument('-l', '--log', default='pynfact.err',
                        help="set a new error log filename (or 'none')")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase output verbosity")
    args = parser.parse_args()

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

