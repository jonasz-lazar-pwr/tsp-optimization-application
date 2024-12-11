// src/tsp_algorithms/bindings/SimulatedAnnealingBindings.cpp

#include "SimulatedAnnealing.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// Using pybind11 namespace for convenience
namespace py = pybind11;

PYBIND11_MODULE(tsp_sa, m) {
    // Define the InitialTempMethodSA enum to expose to Python
    py::enum_<InitialTempMethodSA>(m, "InitialTempMethodSA")
        .value("AVG", InitialTempMethodSA::AVG)
        .value("MAX", InitialTempMethodSA::MAX)
        .value("SAMPLING", InitialTempMethodSA::SAMPLING)
        .export_values();

    // Define the MoveTypeSA enum to expose to Python
    py::enum_<NeighborSelectionMethodSA>(m, "NeighborSelectionMethodSA")
        .value("SWAP", NeighborSelectionMethodSA::SWAP)
        .value("INSERT", NeighborSelectionMethodSA::INSERT)
        .value("INVERT", NeighborSelectionMethodSA::INVERT)
        .export_values();

    // Define the InitialSolutionMethodSA enum to expose to Python
    py::enum_<InitialSolutionMethodSA>(m, "InitialSolutionMethodSA")
        .value("RANDOM", InitialSolutionMethodSA::RANDOM)
        .value("GREEDY", InitialSolutionMethodSA::GREEDY)
        .export_values();

    // Expose the SimulatedAnnealing class and bind its methods and constructor
    py::class_<SimulatedAnnealing>(m, "SimulatedAnnealing")
        // Binding constructor with enums and relevant parameters
        .def(py::init<int, int, const std::vector<std::vector<int>>&, int, InitialTempMethodSA,
            InitialSolutionMethodSA, NeighborSelectionMethodSA, int, double>(),
            py::arg("port"),
            py::arg("data_frequency_ms"),
            py::arg("dist_matrix"),
            py::arg("duration_ms"),
            py::arg("initial_temp_method"),
            py::arg("initial_solution_method"),
            py::arg("neighbor_selection_method"),
            py::arg("steps_per_temp"),
            py::arg("alpha"),
            "Initialize the Simulated Annealing algorithm with the given parameters.")

        // Binding for running the algorithm
        .def("run", &SimulatedAnnealing::run, "Run the Simulated Annealing algorithm.");
}
