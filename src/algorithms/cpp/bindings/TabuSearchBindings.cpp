// src/algorithms/cpp/bindings/TabuSearchBindings.cpp

#include "TabuSearch.h"
#include "MoveType.h"
#include "TenureType.h"
#include "TabuListLimitType.h"
#include "InitialSolutionType.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// Using pybind11 namespace for convenience
namespace py = pybind11;

PYBIND11_MODULE(TabuSearch, m) {
    // Define the MoveType enum to expose to Python
    py::enum_<MoveType>(m, "MoveType")
        .value("SWAP", MoveType::SWAP)
        .value("OPT_2", MoveType::OPT_2)
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
    py::enum_<InitialSolutionType>(m, "InitialSolutionType")
        .value("RANDOM", InitialSolutionType::RANDOM)
        .value("GREEDY", InitialSolutionType::GREEDY)
        .export_values();

    // Expose the TabuSearch class and bind its methods and constructor
    py::class_<TabuSearch>(m, "TabuSearch")
        // Binding constructor with optional random_tenure_range and tenure_type
        .def(py::init<int, const std::vector<std::vector<int>>&, MoveType, int,
                      std::pair<int, int>, TenureType, TabuListLimitType, int, int,
                      InitialSolutionType>(),
             py::arg("tenure"), py::arg("dist_matrix"),
             py::arg("move_type"), py::arg("duration_ms"),
             py::arg("random_tenure_range") = std::make_pair(0, 0),
             py::arg("tenure_type") = TenureType::CONSTANT,
             py::arg("limit_type") = TabuListLimitType::N,
             py::arg("custom_limit") = 0,
             py::arg("max_neighbors") = 100,
                py::arg("initial_solution_type") = InitialSolutionType::GREEDY,
             "Initialize the Tabu Search algorithm with the given parameters.")

        // Binding for running the algorithm
        .def("run", &TabuSearch::run, "Run the Tabu Search algorithm.");
}
