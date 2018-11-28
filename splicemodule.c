#define _GNU_SOURCE

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// TODO: comments and explanation
// TODO: conditionals for different distros
// TODO: function declarations for all
// TODO: sane perror args
// TODO: structure error handling part

// function declarations
size_t fsize(int);
int is_fd_valid(int);
PyMODINIT_FUNC PyInit_splice();
size_t splice_copy(int, int, int, size_t);
static PyObject *method_splice(PyObject *, PyObject *);

// return size of file using file descriptor 
size_t 
fsize(fd)
{
    size_t fsize;
    fsize = lseek(fd, 0, SEEK_END);
    return fsize;
}

// check if file descriptor is valid
int 
is_fd_valid(fd)
{
  return fcntl(fd, F_GETFD);
}

// splice(2) syscall
size_t 
splice_copy(int fd_in, int fd_out, int offset, size_t len)
{
    int fd_pipe[2];
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
      
      // splice data to pipe
      if ((bytes = splice(fd_in, &in_off, fd_pipe[1], NULL, buf_size, SPLICE_F_MOVE)) == -1)
      {
        perror("Error moving data from `fd_in`");
        return -1;
      }

      // splice data from pipe to fd_out
      if ((bytes = splice(fd_pipe[0], NULL, fd_out, &out_off, buf_size, SPLICE_F_MOVE)) == -1)
      {
        perror("Error moving data to `fd_out`");
        return -1;
      }

      len -= buf_size;
      total_bytes_sent += bytes;
    }
    return total_bytes_sent;
}

static PyObject *
method_splice(PyObject *self, PyObject *args)
{
    int fd_in, fd_out, offset, nbytes;
    int status = -1;
    size_t len;

    if (!PyArg_ParseTuple(args, "iiii", &fd_in, &fd_out, &offset, &nbytes))
    {
            return NULL;
    }

    if (is_fd_valid(fd_in) == -1 || is_fd_valid(fd_out) == -1)
    {
      PyErr_SetString(PyExc_ValueError, "Invalid file descriptor");
      return NULL;
    }

    if (nbytes)
    {
      if (nbytes > fsize(fd_in))
      {
        PyErr_SetString(PyExc_OverflowError, "Length overflow error");
        return NULL;
      }
      len = nbytes;
    }
    else
    {
      len = (size_t)fsize(fd_in);
    }
    
    if (offset > len)
    {
      PyErr_SetString(PyExc_OverflowError, "Offset overflow error");
      return NULL;
    }

    status = splice_copy(fd_in, fd_out, offset, len);
    
    return PyLong_FromLong(status);
}

static PyMethodDef SpliceMethods[] = {
    {"splice",  method_splice, METH_VARARGS, "Python interace for splice(2) system call."},
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
    return PyModule_Create(&splicemodule);
}

int main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);

    if (program == NULL)
    {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }


    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("splice", PyInit_splice);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("splice");

    PyMem_RawFree(program);

    return 0;
}
