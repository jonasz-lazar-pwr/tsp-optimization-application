// src/tsp_algorithms/bindings/SimulatedAnnealingBindings.cpp

#include "SimulatedAnnealing.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// Using pybind11 namespace for convenience
namespace py = pybind11;

PYBIND11_MODULE(tsp_sa, m) {
    // Define the InitialTempType enum to expose to Python
    py::enum_<InitialTempType>(m, "InitialTempType")
        .value("AVG", InitialTempType::AVG)
        .value("MAX", InitialTempType::MAX)
        .value("SAMPLING", InitialTempType::SAMPLING)
        .export_values();

    // Define the TempDecayType enum to expose to Python
    py::enum_<TempDecayType>(m, "TempDecayType")
        .value("GEO", TempDecayType::GEO)
        .value("LOG", TempDecayType::LOG)
        .value("LINE", TempDecayType::LINE)
        .export_values();

    // Define the MoveTypeSA enum to expose to Python
    py::enum_<MoveTypeSA>(m, "MoveType")
        .value("SWAP", MoveTypeSA::SWAP)
        .value("INSERT", MoveTypeSA::INSERT)
        .value("INVERT", MoveTypeSA::INVERT)
        .export_values();

    // Define the InitialSolutionTypeSA enum to expose to Python
    py::enum_<InitialSolutionTypeSA>(m, "InitialSolutionType")
        .value("RANDOM", InitialSolutionTypeSA::RANDOM)
        .value("GREEDY", InitialSolutionTypeSA::GREEDY)
        .export_values();

    // Expose the SimulatedAnnealing class and bind its methods and constructor
    py::class_<SimulatedAnnealing>(m, "SimulatedAnnealing")
        // Binding constructor with enums and relevant parameters
        .def(py::init<int, int, const std::vector<std::vector<int>>&, InitialTempType,
            TempDecayType, double, double, int, MoveTypeSA, InitialSolutionTypeSA>(),
            py::arg("duration_ms"),
            py::arg("port"),
            py::arg("dist_matrix"),
            py::arg("initial_temp_type"),
            py::arg("temp_decay_type"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("steps_per_temp"),
            py::arg("move_type"),
            py::arg("initial_solution_type"),
            "Initialize the Simulated Annealing algorithm with the given parameters.")

        // Binding for running the algorithm
        .def("run", &SimulatedAnnealing::run, "Run the Simulated Annealing algorithm.");
}
