// src/tsp_algorithms/bindings/TabuSearchBindings.cpp

#include "TabuSearch.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// Using pybind11 namespace for convenience
namespace py = pybind11;

PYBIND11_MODULE(tsp_ts, m) {
    // Define the MoveType enum to expose to Python
    py::enum_<NeighborSelectionMethodTS>(m, "NeighborSelectionMethodTS")
        .value("SWAP", NeighborSelectionMethodTS::SWAP)
        .value("OPT_2", NeighborSelectionMethodTS::OPT_2)
        .export_values();

    // Define the TabuListLimitMethodTS enum to expose to Python
    py::enum_<TabuListLimitMethodTS>(m, "TabuListLimitMethodTS")
        .value("N", TabuListLimitMethodTS::N)
        .value("SQRT_N", TabuListLimitMethodTS::SQRT_N)
        .value("THREE_N", TabuListLimitMethodTS::THREE_N)
        .value("N_SQUARED", TabuListLimitMethodTS::N_SQUARED)
        .value("CUSTOM", TabuListLimitMethodTS::CUSTOM)
        .export_values();

    // Define the InitialSolutionType enum to expose to Python
    py::enum_<InitialSolutionMethodTS>(m, "InitialSolutionMethodTS")
        .value("RANDOM", InitialSolutionMethodTS::RANDOM)
        .value("GREEDY", InitialSolutionMethodTS::GREEDY)
        .export_values();

    // Define the TenureType enum to expose to Python
    py::enum_<TenureTypeTS>(m, "TenureTypeTS")
        .value("CONSTANT", TenureTypeTS::CONSTANT)
        .value("RANDOM", TenureTypeTS::RANDOM)
        .export_values();

    // Expose the TabuSearch class and bind its methods and constructor
    py::class_<TabuSearch>(m, "TabuSearch")
        // Binding constructor with enums and relevant parameters
        .def(py::init<int, int, const std::vector<std::vector<int>>&, int, InitialSolutionMethodTS,
            NeighborSelectionMethodTS, int, TabuListLimitMethodTS, int, TenureTypeTS, int, std::pair<int, int>>(),
            py::arg("port"),
            py::arg("data_frequency_ms"),
            py::arg("dist_matrix"),
            py::arg("duration_ms"),
            py::arg("initial_solution_method"),
            py::arg("neighbor_selection_method"),
            py::arg("max_neighbors"),
            py::arg("tabu_list_limit_method"),
            py::arg("tabu_list_custom_limit"),
            py::arg("tenure_type"),
            py::arg("constant_tenure"),
            py::arg("random_tenure_range"),
            "Initialize the Tabu Search algorithm with the given parameters.")

        // Binding for running the algorithm
        .def("run", &TabuSearch::run, "Run the Tabu Search algorithm.");
}
