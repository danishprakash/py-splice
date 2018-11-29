======
splice
======

A Python interface to splice(2) system call

=====
About
=====

`splice() <http://man7.org/linux/man-pages/man2/splice.2.html>`__ moves
data between two file descriptors without copying between kernel
address space and user address space.  It transfers up to len bytes
of data from the file descriptor fd_in to the file descriptor fd_out,
where one of the file descriptors must refer to a pipe.

Zero-copy
---------
Ideally when you copy data from one data stream to another, the data
to be copied is first stored in a buffer in userspace and then it is
again copied back to the target data stream from the user space. This
introduces a certain overhead which stems from copying of data to and 
from the userspace.

Zero-copy allows us to operate on data without the use of copying 
data to userspace. It essentialy copies the data by remapping pages
and not actually performing the copying of data, resulting in 
improved performance.

.. code-block:: python

    # copy data from one file to another

    from splice import splice

    to_read = open("read.txt") # file to read from
    to_write = open("write.txt", "w+") # file to write to

    # pass file descriptors
    splice(to_read.fileno(), to_write.fileno(), offset, flags)


This copying of the data twice (once into the userland buffer, and once out
from that userland buffer) imposes some performance and resource penalties.
`splice(2) <http://linux.die.net/man/2/splice>`__ syscall avoids these
penalties by avoiding any use of userland buffers; it also results in a single
system call (and thus only one context switch), rather than the series of
`read(2) <http://linux.die.net/man/2/read>`__ /
`write(2) <http://linux.die.net/man/2/write>`__ system calls (each system call
requiring a context switch) used internally for the data copying.


=================
API Documentation
=================

sendfile module provides a single function: sendfile().

- ``splice.splice(out, in, offset, nbytes, flags=0)``

  Copy *nbytes* bytes from file descriptor *in* (a regular file) to file
  descriptor *out* (a regular file) starting at *offset*. Return the number of
  bytes just being sent. When the end of file is reached return 0.
  On Linux, if *offset* is given as *None*, the bytes are read from the current
  position of *in* and the position of *in* is updated.
  *headers* and *trailers* are strings that are written before and after the
  data from *in* is written. In cross platform applications their usage is
  discouraged

- ``splice.SPLICE_F_MOVE``
- ``splice.SPLICE_F_NONBLOCK``
- ``splice.SPLICE_F_MORE``
- ``splice.SPLICE_F_GIFT``


=====================
Why would I use this?
=====================
By not interacting with userspace while copying data betweek files, ``splice(2)``
is said to perform. There is no benchmark for this available yet,
but I'm looking at writing a simple benchmark script for this, similar to
`this <url>`__. 


===================
Supported platforms
===================

This system call is (GNU)Linux-specific. 

=======
Support
=======

Feel free to add improvements, report issues or contact me about anything related to the project.

=======
LICENSE
=======

MIT
