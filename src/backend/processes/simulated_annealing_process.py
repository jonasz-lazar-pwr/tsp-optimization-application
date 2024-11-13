# src/backend/processes/simulated_annealing_process.py

from multiprocessing import Queue, Barrier
from src.backend.processes.base_algorithm_process import BaseAlgorithmProcess
from src.backend.components.sa_parameters import map_initial_temp_method, map_neighbor_selection_method, \
    map_initial_solution_method

import compiled_binaries.tsp_sa as sa


class SimulatedAnnealingProcess(BaseAlgorithmProcess):
    def __init__(self, port: int, data_frequency: int, distance_matrix: list[list[int]],
                 queue: Queue, start_barrier: Barrier, config_params) -> None:
        """
        Initializes the SimulatedAnnealingProcess with the necessary parameters, including the communication port,
        data frequency, distance matrix, queue, synchronization barrier, and configuration parameters for the algorithm.

        :param port: The port used for NNG socket communication between processes.
        :param data_frequency: The frequency in milliseconds at which data is sent.
        :param distance_matrix: The distance matrix representing distances between cities in the TSP problem.
        :param queue: The multiprocessing queue used to transmit data between processes.
        :param start_barrier: The barrier for synchronizing the start of multiple processes.
        :param config_params: Configuration parameters for the Simulated Annealing algorithm.
        :return: None
        """
        super().__init__(port, data_frequency, distance_matrix, queue, start_barrier, config_params)


    def run_algorithm(self) -> None:
        """
        Executes the Simulated Annealing algorithm, using C++ bindings for performance. This function:
        1. Waits at the start barrier for other processes to synchronize.
        2. Maps custom Python enum types for initial temperature, initial solution, and neighbor selection methods
           to their C++ equivalents.
        3. Initializes a SimulatedAnnealing instance with the mapped parameters and other configuration values.
        4. Calls the `run` method on the SimulatedAnnealing instance, which executes the algorithm.

        :return: None
        """
        # Wait for other processes to reach the barrier before starting
        self.start_barrier.wait()

        # Convert custom Python enum types to their corresponding C++ values
        initial_temp_method_cpp = map_initial_temp_method(self.config_params.initial_temp_method)
        initial_solution_method_cpp = map_initial_solution_method(self.config_params.initial_solution_method)
        neighbor_selection_method_cpp = map_neighbor_selection_method(self.config_params.neighbor_selection_method)

        # Initialize the Simulated Annealing instance with algorithm parameters
        sa_instance = sa.SimulatedAnnealing(
            port=self.port,
            data_frequency_ms=self.data_frequency,
            dist_matrix=self.distance_matrix,
            duration_ms=self.config_params.duration_ms,
            initial_temp_method=initial_temp_method_cpp,
            initial_solution_method=initial_solution_method_cpp,
            neighbor_selection_method=neighbor_selection_method_cpp,
            steps_per_temp=self.config_params.steps_per_temp,
            alpha=self.config_params.alpha,
        )

        # Run the Simulated Annealing algorithm
        sa_instance.run()
