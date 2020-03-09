from setuptools import setup, find_packages

setup(name='pynfact',
      packages=['pynfact'],
      version='0.4.0',
      author='J. A. Corbal',
      author_email='jacorbal@gmail.com',
      description='Blog-oriented static web generator',
      long_description=open('README').read(),
      keywords = ['blog', 'static', 'web', 'generator'],
      license='MIT',
      py_modules=find_packages(),
      scripts = ['bin/run-pynfact'],
      entry_points = { 'console_scripts': [ 'main = pynfact.cli:main' ] } )

