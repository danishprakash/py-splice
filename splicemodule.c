#define _GNU_SOURCE

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// TODO: custom exceptions
// TODO: comments and explanation
// TODO: conditionals for different distros
// TODO: better return mechanism
// TODO: function declarations for all
// TODO: abide by code guidelines for C programming language
// TODO: make `from pysplice import splice` work
// TODO: Write tests

// return size of file using file descriptor number
size_t fsize(fd) {
    size_t fsize;
    fsize = lseek(fd, 0, SEEK_END);
    return fsize;
}

// move data from fd_in tp fd_out using splice(2)
ssize_t splice_copy(int fd_in, int fd_out) {
    int fd_pipe[2];
    size_t buf_size = 128;
    size_t len = fsize(fd_in);
    size_t bytes = 0;
    loff_t in_off = 0;
    loff_t out_off = 0;

    if (pipe(fd_pipe) < 0) {
        perror("Error creating pipe");
        return 1;
    }


    while(len > 0) {
      if (buf_size > len) buf_size = len;
      // splice data to pipe
      if ((bytes = splice(fd_in, &in_off, fd_pipe[1], NULL, buf_size, SPLICE_F_MOVE)) == -1) {
        perror("splice");
        return -1;
      }


        // splice data from pipe to fd_out
        if ((bytes = splice(fd_pipe[0], NULL, fd_out, &out_off, buf_size, SPLICE_F_MOVE)) == -1) {
            perror("splice");
            return -1;
        }

        len -= buf_size;
    }
    return bytes;
}

// TODO: check for splice(2) availability
static PyObject *
method_splice(PyObject *self, PyObject *args){
    int fd_in, fd_out;
    int status = -1;

    if (!PyArg_ParseTuple(args, "ii", &fd_in, &fd_out))
            return NULL;

    status = splice_copy(fd_in, fd_out);
    
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
PyInit_splice(void) {
    return PyModule_Create(&splicemodule);
}

int main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
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
