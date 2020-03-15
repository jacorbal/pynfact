#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8 tw=72 fdm=indent nowrap:
"""
    pynfact.cli
    ~~~~~~~~~~~

    Command line interface.
    
    :copyright: © 2012-2020, J. A. Corbal
    :license: MIT
"""
from pynfact.builder import Builder
from pynfact.server import Server
from pynfact.yamler import Yamler
import logging
import os
import shutil
import sys


try:
    import colored_traceback.auto
    colored_traceback.add_hook(always=True)
except ImportError:
    pass


def show_help():
    """Display help on screen."""
    print("  $ pynfact init [<site>]. Creates new empty site\n"
          "  $ pynfact build......... Builds site\n"
          "  $ pynfact serve......... Testing server\n"
          "  $ pynfact help.......... Displays this awesome help\n")


def set_logger(default_level=logging.INFO, warning_log='pynfact.err',
               echo_log=sys.stdout):
    """Setup the system logger.

    :param default_level: Log level for the default echo logger
    :type default_level: int, str
    :param warning_log: Filename for the warnings and errors log
    :type warning_log: str
    :param echo_log: Where to write the default notification log
    :type echo_log: str

    The default levels are set by the ``logging`` module.  It can be
    specify by integer value or by name.  These are the options:

    * 10: ``logging.DEBUG``
    * 20: ``logging.INFO``
    * 30: ``logging.WARNING``
    * 40: ``logging.ERROR``
    * 50: ``logging.CRITICAL``

    This log is intended to print information to ``stdout`` is
    ``echo_log``, and it may take any value for the log level.  It's
    specially useful when debugging, but it's intended value is just
    information, but less useful when set to a log level higher than
    ``loging.WARNING``, for the ``warning_log`` is already taking care
    of those logs.

    .. note:: The ``echo_log`` is a stream handler, so the file will not
              be closed at the end.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(default_level)

    # Default ``stdout`` handler, set by function caller
    echo_shandler = logging.StreamHandler(echo_log)
    echo_shandler.setLevel(default_level)
    echo_shandler.setFormatter(logging.Formatter(
        '[%(levelname)s]: %(message)s'))

    # Warnings and Errors handler (write to file)
    warning_fhandler = logging.FileHandler(warning_log)
    warning_fhandler.setLevel(logging.WARNING)
    warning_fhandler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s]: %(message)s'))

    logger.addHandler(echo_shandler)
    logger.addHandler(warning_fhandler)

    return logger


def retrieve_config(config_file, logger=None):
    """
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


def main():
    """Main entry."""
    # Logger setup (set parameter to ``None`` to deactivate all logging)
    logger = set_logger(logging.INFO)

    # Extension setup
    default_content_ext = '.md'  # .mkdn, .markdown,...

    # Argument management (TODO: use `argparse`)
    if len(sys.argv) >= 2:
        action = sys.argv[1]
    else:
        action = "help"

    if action == "init" or action == "new":
        real_path = os.path.dirname(os.path.realpath(__file__))
        src = os.path.join(real_path, 'initnew')
        dst = 'pynfact_blog' if len(sys.argv) < 3 else sys.argv[2]

        # create new blog structure with the default values
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            error_msg = "Cannot make blog structure"
            if logger:
                logger.error(error_msg)
            sys.exit(error_msg)

    elif action == "help":
        show_help()

    elif action == "serve":
        port = 4000 if len(sys.argv) < 3 else int(sys.argv[2])
        server = Server('127.0.0.1', port=port, path='_build',
                        logger=logger)
        server.serve()

    elif action == "build":
        config_file = 'config.yml' if len(sys.argv) < 3 else sys.argv[2]
        site_config = retrieve_config(config_file, logger)

        # Prepare builder
        template_values = {'blog': {
            'author': site_config['info']['site_author'],
            'base_uri': site_config['uri']['base'],
            'encoding': site_config['wlocale']['encoding'],
            'feed_format': site_config['presentation']['feed_format'],
            'lang': site_config['wlocale']['language'],
            'site_name': site_config['info']['site_name'],
            'page_links': [],
        }}

        # Build
        b = Builder(site_config, template_values,
                    infile_ext=default_content_ext, logger=logger)
        b.gen_site()


# Main entry
if __name__ == "__main__":
    main()

