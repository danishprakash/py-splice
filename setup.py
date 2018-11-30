#!/usr/bin/env python3

from distutils.core import setup, Extension

NAME = 'py-splice'
VERSION = '1.0.1'


def main():
    setup(name=NAME,
          url='https://github.com/danishprakash/py-splice',
          version=VERSION,
          description='A Python interface to splice(2)',
          long_description=open('README.rst', 'r').read(),
          author='Danish Prakash',
          author_email='danishprakash <at> outlook <dot> com',
          platforms='UNIX',
          license='GPL',
          keywords=['splice', 'python', 'performance', 'zero-copy'],
          ext_modules=[Extension('splice', ['splicemodule.c'])],
          classifiers=['Development Status :: 4 - Beta',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                       'Operating System :: POSIX :: Linux',
                       'Programming Language :: C',
                       'Programming Language :: Python :: 3.0',
                       'Programming Language :: Python :: 3.1',
                       'Programming Language :: Python :: 3.2',
                       'Programming Language :: Python :: 3.3',
                       'Programming Language :: Python :: 3.4',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Topic :: Software Development :: Libraries :: Python Modules',
                       'Topic :: System :: Filesystems',
                       'Topic :: System :: Operating System',
                       'Topic :: System :: Operating System Kernels :: Linux'])


if __name__ == '__main__':
    main()
