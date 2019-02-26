# vim: ft=python:fenc=utf-8:tw=72:fdm=indent:nowrap
# -*- coding: utf-8 -*-
"""
    pyblic.yamler
    ~~~~~~~~~~~~~

    Handles a YAML file by setting a default value when variable
    is not set.

    :copyright: (c) 2012-2019, J. A. Corbal
    :license: 3-clause license ("Modified BSD License")
"""
import sys
import yaml


class Yamler:
    """Handles a YAML file."""

    def __init__(self, filename):
        """Initializer.

        :param filename: YAML filename where to look for the config.
        :type filename: str
        """
        self.filename = filename
        try:
            self.fd = open(self.filename, 'r')
            self.config = yaml.load(self.fd)
        except IOError:
            sys.stderr.write("Error, config file is aready open")


    def __del__(self):
        """Destructor."""
        self.fd.close()


    def __getitem__(self, key):
        try:
            value = self.config[key]
        except KeyError:
            sys.stderr.write("Error, Key not found")
        else:
            return value

    def retrieve(self, key, default_value=None):
        """Gets a value from a key or sets a default value."""
        try:
            value = self.config[key]
        except KeyError:
            value = default_value
        else:
            return value

