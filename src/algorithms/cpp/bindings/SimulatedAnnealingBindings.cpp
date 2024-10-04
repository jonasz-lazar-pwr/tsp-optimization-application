// src/algorithms/cpp/bindings/SimulatedAnnealingBindings.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "SimulatedAnnealing.h"

// Using pybind11 namespace for convenience
namespace py = pybind11;

// Define the Python module and expose the SimulatedAnnealing class
PYBIND11_MODULE(SimulatedAnnealing, m) {
    py::class_<SimulatedAnnealing>(m, "SimulatedAnnealing")
        // Constructor binding, allowing initialization with specific parameters
        .def(py::init<double, double, const std::vector<std::vector<double>>&,
                      const std::string&, const std::string&, const std::string&, double, double, int>(),
             py::arg("final_temp"), py::arg("duration"), py::arg("dist_matrix"),
             py::arg("temp_init_method"), py::arg("temp_decay_method"), py::arg("neighbor_method"),
             py::arg("alpha"), py::arg("beta"), py::arg("steps_per_temp"),
             "Initialize the Simulated Annealing algorithm with specific parameters.")

        // Binding the 'run' method to execute the Simulated Annealing algorithm and return the final cost
        .def("run", &SimulatedAnnealing::run, "Run the Simulated Annealing algorithm and return the final cost.")

        // Accessor to retrieve the current solution's cost, calculated using the calculate_cost method
        .def_property_readonly("current_cost", [](const SimulatedAnnealing& sa) {
            return sa.calculate_cost(sa.get_current_solution());
        }, "Retrieve the cost of the current solution.")

        // Accessor to retrieve the current solution vector
        .def_property_readonly("current_solution", &SimulatedAnnealing::get_current_solution,
            "Retrieve the current solution vector.");
}