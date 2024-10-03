// src/algorithms/cpp/bindings/SimulatedAnnealingBindings.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "SimulatedAnnealing.h"

namespace py = pybind11;

PYBIND11_MODULE(SimulatedAnnealing, m) {
    py::class_<SimulatedAnnealing>(m, "SimulatedAnnealing")
        .def(py::init<double, int, const std::vector<std::vector<double>>&>())  // Initialize with temp, iterations, distance matrix
        .def("run", &SimulatedAnnealing::run)  // Run the algorithm
        .def("iterate", &SimulatedAnnealing::iterate)  // Iterate through the algorithm
        .def("get_max_iterations", &SimulatedAnnealing::get_max_iterations);  // Add getter for max_iterations
}