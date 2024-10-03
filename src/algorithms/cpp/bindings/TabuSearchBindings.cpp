// src/algorithms/cpp/bindings/TabuSearchBindings.cpp

#include <pybind11/pybind11.h>
#include "TabuSearch.h"

namespace py = pybind11;

PYBIND11_MODULE(TabuSearch, m) {
    py::class_<TabuSearch>(m, "TabuSearch")
        .def(py::init<>())  // Konstruktor
        .def("run", &TabuSearch::run);  // Powiązanie metody run
}
