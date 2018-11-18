#include <Python.h>

static PyObject *SpliceError;

static PyObject *
method_splice(PyObject *self, PyObject *args){
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
            return NULL;

    sts = system(command);
    if (sts < 0) {
        PyErr_SetString(SpliceError, "Error executing splice(2) system call");
        return NULL;
    }

    return PyLong_FromLong(sts);
}

static PyMethodDef SpliceMethods[] = {
    {"splice",  method_splice, METH_VARARGS, "Python interace for splice(2) system call."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef splicemodule = {
    PyModuleDef_HEAD_INIT,
    "splice",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    SpliceMethods
};

PyMODINIT_FUNC
PyInit_splice(void) {
    return PyModule_Create(&splicemodule);
}

int
main(int argc, char *argv[])
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
