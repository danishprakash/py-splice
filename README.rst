.. image:: http://pepy.tech/badge/py-splice
    :target: http://pepy.tech/project/py-splice/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/py-splice.svg
    :target: https://pypi.python.org/pypi/py-splice/
    :alt: Latest version 

.. image:: https://img.shields.io/pypi/l/py-splice.svg
    :target: https://pypi.python.org/pypi/py-splice/
    :alt: License


splice
======

A Python interface to splice(2) system call.

About
-----
`splice(2) <http://man7.org/linux/man-pages/man2/splice.2.html>`__ moves
data between two file descriptors without copying between kernel
address space and user address space.  It transfers up to ``nbytes`` bytes
of data from the file descriptor ``in`` to the file descriptor ``out``.

zero-copy
---------
Normally when you copy data from one data stream to another, the data
to be copied is first stored in a buffer in userspace and is then
copied back to the target data stream from the user space which
introduces a certain overhead.

zero-copy allows us to operate on data without the use of copying 
data to userspace. It essentialy transfers the data by remapping pages
and not actually performing the copying of data, resulting in 
improved performance.

Illustrated below is a simple example of copying data from one file
to another using the ``splice(2)`` system call. For the complete documentation
see `API Documentation`_.

.. code-block:: python

    # copy data from one file to another using splice

    from splice import splice

    to_read = open("read.txt")
    to_write = open("write.txt", "w+")

    splice(to_read.fileno(), to_write.fileno())


This copying of the data twice (once into the userland buffer, and once out
from that userland buffer) imposes some performance and resource penalties.
`splice(2) <http://linux.die.net/man/2/splice>`__ syscall avoids these
penalties by avoiding any use of userland buffers; it also results in a single
system call (and thus only one context switch), rather than the series of
`read(2) <http://linux.die.net/man/2/read>`__ /
`write(2) <http://linux.die.net/man/2/write>`__ system calls (each system call
requiring a context switch) used internally for the data copying.

Installation
------------

**pip**

.. code-block:: sh

    $ pip install py-splice


**manual**

.. code-block:: sh

    $ git clone https://github.com/danishprakash/py-splice && cd py-splice
    $ python3 setup.py install


API Documentation
-----------------

sendfile module provides a single function: sendfile().

* ``splice.splice(out, in, offset, nbytes, flags)``

  Copy *nbytes* bytes from file descriptor *in* (a regular file) to file
  descriptor *out* (a regular file) starting at *offset*. Return the number of
  bytes just being sent. When the end of file is reached return 0.
  If *offset* is not specified, the bytes are read from the current
  position of *in* and the position of *in* is updated. If *nbytes* is
  not specified, the whole of *in* is copied over to *out*.

  **Required arguments**
  
  - ``in``: file descriptor of the file from which data is to be read.
  - ``out``: file descriptor of the file to which data is to be transferred.

  **Optional positional arguments**
  
  - ``offset``: offset from where the input file is read from.
  - ``nbytes``: number of bytes to be copied in total, default value
  - ``flags``: a bit mask which can be composed by ORing together the following.
  
      + ``splice.SPLICE_F_MOVE``
      + ``splice.SPLICE_F_NONBLOCK``
      + ``splice.SPLICE_F_MORE``
      + ``splice.SPLICE_F_GIFT``

  More information on what each of the flag means can be found on the splice(2)
  man page `here <http://man7.org/linux/man-pages/man2/splice.2.html>`__.


Usage
-----

.. code-block:: python

    >>> from splice import splice

    # init file objects
    >>> to_read = open("read.txt") # file to read from
    >>> to_write = open("write.txt", "w+") # file to write to

    >>> len(to_read.read())
    50

    # copying whole file
    >>> splice(to_read.fileno(), to_write.fileno())
    50  # bytes copied

    # copying file starting from an offset
    >>> splice(to_read.fileno(), to_write.fileno(), offset=10)
    40

    # copying certain amount of bytes
    >>> splice(to_read.fileno(), to_write.fileno(), nbytes=20)
    20

    # copying certain amount of bytes beginning from an offset
    >>> splice(to_read.fileno(), to_write.fileno(), offset=10, nbytes=20)
    20

    # specifying flags
    >>> import splice
    >>> splice(to_read.fileno(), to_write.fileno(), flags=splice.SPLICE_F_MORE)
    50


Why would I use this?
---------------------
``splice(2)`` is supposed to be better in terms of performance when compared
to traditional read/write methods since it avoids overhead of copying the
data to user address space and instead, does the transfer by remapping pages
in kernel address space. There can be many uses for this especially if
performance is important to the task at hand.


Supported platforms
-------------------
The ``splice(2)`` system call is (GNU)Linux-specific.


Support
-------
Feel free to add improvements, report issues or contact me about anything related to the project.


LICENSE
-------
GNU GPL

