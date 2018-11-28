#!/usr/bin/env python3

from distutils.core import setup, Extension

NAME = 'splice'
VERSION = '1.0.1'


def main():
    setup(name=NAME,
          url='https://github.com/danishprakash/python-splice',
          version=VERSION,
          description='A Python interface to splice(2)',
          long_description=open('README.rst', 'r').read(),
          author='Danish Prakash',
          author_email='danishprakash <at> outlook <dot> com',
          platforms='UNIX',
          license='GPL',
          keywords=['splice', 'python', 'performance', 'zero-copy'],
          ext_modules=[Extension("splice", ["splicemodule.c"])])


if __name__ == '__main__':
    main()
