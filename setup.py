#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8:

from setuptools import setup, find_packages


version = '1.0.1.dev1'

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='pynfact',
      version=version,
      author='J. A. Corbal',
      author_email='jacorbal@gmail.com',
      url='https://github.com/jacorbal/pynfact/wiki',
      download_url='https://github.com/jacorbal/pynfact',
      description='Blog-oriented static web generator using Jinja2 templates',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      keywords = ['blog', 'markdown', 'static', 'web', 'site', 'generator'],
      py_modules=find_packages(),
      packages=['pynfact'],
      entry_points = { 'console_scripts': [ 'main = pynfact.cli:main' ] },
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Text processing :: Blog',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
      ],
      install_requires=[
        'markdown',
        'unidecode',
        'feedgen',
        'jinja2'
      ],
      python_requires='>=3.4',
     )

