#define _GNU_SOURCE

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/* TODO: comments and explanation */
/* TODO: conditionals for different distros */
/* TODO: pass flags to splice(2) calls */

/* function declarations */
size_t fsize(int);
int is_fd_valid(int);
PyMODINIT_FUNC PyInit_splice();
size_t splice_copy(int, int, int, size_t);
int validate_arguments(int, int, int, int *);
static PyObject *method_splice(PyObject *, PyObject *, PyObject *);

/* return size of file using file descriptor  */
size_t 
fsize(fd)
{
    size_t fsize;
    fsize = lseek(fd, 0, SEEK_END);
    return fsize;
}

/* check if file descriptor is valid */
int 
is_fd_valid(fd)
{
    return fcntl(fd, F_GETFD);
}

/* splice(2) syscall */
size_t 
splice_copy(int fd_in, int fd_out, int offset, size_t len)
{
    int fd_pipe[2];
    int flags = 0;
    size_t buf_size = 4096;
    size_t bytes = 0;
    size_t total_bytes_sent = 0;
    off_t in_off = (off_t)offset;
    off_t out_off = 0;

    if (pipe(fd_pipe) < 0)
    {
        perror("Error creating pipe");
        return 1;
    }

    while(len > 0)
    {
        if (buf_size > len) buf_size = len;

        /* splice data to pipe */
        bytes = splice(fd_in, &in_off, fd_pipe[1], NULL, buf_size, flags);
        if (bytes == -1)
        {
            perror("Error moving data from `fd_in`");
            return -1;
        }

        /* splice data from pipe to fd_out */
        bytes = splice(fd_pipe[0], NULL, fd_out, &out_off, buf_size, flags);
        if (bytes == -1)
        {
            perror("Error moving data to `fd_out`");
            return -1;
        }

        len -= buf_size;
        total_bytes_sent += bytes;
    }
    return total_bytes_sent;
}

/* validate arguments */
/* static PyObject * */
int
validate_arguments(int in, int out, int offset, int *nbytes)
{
    if (is_fd_valid(in) == -1 || is_fd_valid(out) == -1)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid file descriptor");
        return -1;
    }

    if (*nbytes)
    {
        if (*nbytes > fsize(in))
        {
            PyErr_SetString(PyExc_OverflowError, "Length overflow error");
            return -1;
        }
    }
    else
    {
        *nbytes = (size_t)fsize(in);
    }

    if (offset > *nbytes)
    {
        PyErr_SetString(PyExc_OverflowError, "Offset overflow error");
        return -1;
    }
    return 1;
}

static PyObject *
method_splice(PyObject *self, PyObject *args, PyObject *kwdict)
{
    int flag = 0;
    int out = -1, in = -1;
    int status = -1, offset = 0, flags = 0, nbytes = 0;
    static char *keywords[] = {"in", "out", "offset", "nbytes", "flags", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwdict, "ii|iii",
                                     keywords, &in, &out, &offset, &nbytes, &flags))
    {
        return NULL;
    }

    flag = validate_arguments(in, out, offset, &nbytes);
    if (flag == -1) 
    {
        return NULL;
    }

    status = splice_copy(in, out, offset, (size_t)nbytes);

    return PyLong_FromLong(status);
}

static PyMethodDef SpliceMethods[] = {
    {"splice",  method_splice, METH_VARARGS | METH_KEYWORDS, "Python interace for splice(2) system call."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef splicemodule = {
    PyModuleDef_HEAD_INIT,
    "splice",
    NULL, 
    -1,  
    SpliceMethods
};

PyMODINIT_FUNC
PyInit_splice(void)
{
    PyObject *module;
    module = PyModule_Create(&splicemodule);

#ifdef SPLICE_F_MOVE
    PyModule_AddIntConstant(module, "SPLICE_F_MOVE", SPLICE_F_MOVE);
#endif
#ifdef SPLICE_F_NONBLOCK
    PyModule_AddIntConstant(module, "SPLICE_F_NONBLOCK", SPLICE_F_NONBLOCK);
#endif
#ifdef SPLICE_F_MORE
    PyModule_AddIntConstant(module, "SPLICE_F_MORE", SPLICE_F_MORE);
#endif
#ifdef SPLICE_F_GIFT
    PyModule_AddIntConstant(module, "SPLICE_F_GIFT", SPLICE_F_GIFT);
#endif    

    return module;
}
