  /
  def generate_graph(values):
            cell_neighbor_weights = (1, 10, 11)  # Negatives are redundant
            graphs = []
            for value in values:
                for weight in cell_neighbor_weights:
                    if 0 <= value+weight <= 120:
                        in_graphs_flag = False
                        for independent_graph in graphs:
                            if value in independent_graph:
                                if value+weight not in independent_graph:
                                    independent_graph.extend([value+weight])
                                in_graphs_flag = True
                        if in_graphs_flag is False:
                            if value+weight in values:
                                graphs.append([value, value+weight])
                            else:
                                graphs.append([value])
            return graphs

----------------------------------------------------------------------/

#include <Python.h>
 
int Cfib(int n)
{
    if (n < 2)
        return n;
    else
        return Cfib(n-1) + Cfib(n-2);
}


 
static PyObject* fib(PyObject* self, PyObject* args)
{
    int n;
 
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
 
    return Py_BuildValue("i", Cfib(n));
}

-----------------------------------------------------------------------------------
static PyMethodDef myMethods[] = {
    {"fib", fib, METH_VARARGS, "Returns the final graph in a list"},
    {NULL, NULL, 0, NULL}
};
---------------------------------------------------------------------------------- 
static struct PyModuleDef myModule = {
	PyModuleDef_HEAD_INIT,
	"myModule", #name of module.
	"Fibonacci Module",
	-1,
	myMethods
};

PyMODINIT_FUNC PyInit_myModule(void)
{
    return PyModule_Create(&myModule);
}
