#!/usr/bin/env python3
# vim: set ft=python fileencoding=utf-8:

from setuptools import setup, find_packages


version = '1.0.1.dev1'

#with open("README.md", "r") as fh:
#    long_description = fh.read()

long_description = '''Pynfact is a simple static website generator
oriented to chronological content, like blogs or websites with historic
and sequential data.  It allows integration with external scripts,
comment engines such as Disqus, TalkYard, etc., or Google Analytics...
Theming and configuration is possible by editing Jinja2 templates.

The interaction is done by command line.  Only a few commands are
needed:

  * `pynfact init <myblog>`: Create a folder with all needed content
  * Configure settings in `config.yml`, title, name, language...
  * `pynfact build`: Generates the static content
  * `pynfact serve`: Serves locally to test the results
   (by default at `localhost:4000`)

'''


setup(name='pynfact',
      version=version,
      author='J. A. Corbal',
      author_email='jacorbal@gmail.com',
      url='https://github.com/jacorbal/pynfact/wiki',
      download_url = 'https://github.com/jacorbal/pynfact',
      project_urls={
          'Documentation': 'https://github.com/jacorbal/pynfact/wiki',
          'Funding': 'https://jacorbal.es/pynfact',
          'Source': 'https://github.com/jacorbal/pynfact',
          'Tracker': 'https://github.com/jacorbal/pynfact/issues'},
      description='Blog-oriented static web generator using Jinja2 templates.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      keywords=['blog', 'markdown', 'static', 'web', 'site', 'generator'],
      py_modules=find_packages(),
      packages=['pynfact'],
      entry_points={ 'console_scripts': [ 'main = pynfact.cli:main' ] },
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console'
        'Framework :: PynFact',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
      ],
      install_requires=[
        'feedgen >= 0.9.0',
        'jinja2 >= 2.10',
        'markdown >= 3.0.0',
        'pygments >= 2.3.0',
        'unidecode >= 1.0.0',
      ],
      python_requires='>=3.6',
  )

