// src/tsp_algorithms/bindings/TabuSearchBindings.cpp

#include "TabuSearch.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// Using pybind11 namespace for convenience
namespace py = pybind11;

PYBIND11_MODULE(tsp_ts, m) {
    // Define the MoveType enum to expose to Python
    py::enum_<MoveTypeTS>(m, "MoveType")
        .value("SWAP", MoveTypeTS::SWAP)
        .value("OPT_2", MoveTypeTS::OPT_2)
        .export_values();

    // Define the TenureType enum to expose to Python
    py::enum_<TenureType>(m, "TenureType")
        .value("CONSTANT", TenureType::CONSTANT)
        .value("RANDOM", TenureType::RANDOM)
        .export_values();

    // Define the TabuListLimitType enum to expose to Python
    py::enum_<TabuListLimitType>(m, "TabuListLimitType")
        .value("N", TabuListLimitType::N)
        .value("SQRT_N", TabuListLimitType::SQRT_N)
        .value("THREE_N", TabuListLimitType::THREE_N)
        .value("N_SQUARED", TabuListLimitType::N_SQUARED)
        .value("CUSTOM", TabuListLimitType::CUSTOM)
        .export_values();

    // Define the InitialSolutionType enum to expose to Python
    py::enum_<InitialSolutionTypeTS>(m, "InitialSolutionType")
        .value("RANDOM", InitialSolutionTypeTS::RANDOM)
        .value("GREEDY", InitialSolutionTypeTS::GREEDY)
        .export_values();

    // Expose the TabuSearch class and bind its methods and constructor
    py::class_<TabuSearch>(m, "TabuSearch")
        // Binding constructor with enums and relevant parameters
        .def(py::init<int, int, const std::vector<std::vector<int>>&, int, std::pair<int, int>,
            TenureType, TabuListLimitType, int, int, MoveTypeTS, InitialSolutionTypeTS>(),
            py::arg("duration_ms"),
            py::arg("port"),
            py::arg("dist_matrix"),
            py::arg("tenure"),
            py::arg("random_tenure_range"),
            py::arg("tenure_type"),
            py::arg("limit_type"),
            py::arg("custom_limit"),
            py::arg("max_neighbors"),
            py::arg("move_type"),
            py::arg("initial_solution_type"),
            "Initialize the Tabu Search algorithm with the given parameters.")

        // Binding for running the algorithm
        .def("run", &TabuSearch::run, "Run the Tabu Search algorithm.");
}
