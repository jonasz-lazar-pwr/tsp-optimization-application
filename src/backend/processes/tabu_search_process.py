# src/backend/processes/tabu_search_process.py

from multiprocessing import Queue, Barrier
from src.backend.processes.base_algorithm_process import BaseAlgorithmProcess
from src.backend.components.ts_parameters import map_neighbor_selection_method, map_tabu_list_limit_method, \
    map_initial_solution_method, map_tenure_type

import compiled_binaries.tsp_ts as ts


class TabuSearchProcess(BaseAlgorithmProcess):
    def __init__(self, port: int, data_frequency: int, distance_matrix: list[list[int]],
                 queue: Queue, start_barrier: Barrier, config_params) -> None:
        """
        Initializes the TabuSearchProcess with the required parameters, including communication port, data frequency,
        distance matrix, communication queue, synchronization barrier, and configuration parameters for the Tabu Search algorithm.

        :param port: The port used for NNG socket communication between processes.
        :param data_frequency: The frequency in milliseconds for data updates.
        :param distance_matrix: The distance matrix for the TSP problem.
        :param queue: The multiprocessing queue for data communication between processes.
        :param start_barrier: The barrier for synchronizing the start of multiple processes.
        :param config_params: Configuration parameters for the Tabu Search algorithm.
        :return: None
        """
        super().__init__(port, data_frequency, distance_matrix, queue, start_barrier, config_params)


    def run_algorithm(self) -> None:
        """
        Executes the Tabu Search algorithm using C++ bindings for efficiency. This function:
        1. Waits at the start barrier to synchronize with other processes.
        2. Maps custom Python enum types for initial solution, neighbor selection, tabu list limit method, and tenure
            type to their C++ equivalents.
        3. Initializes a TabuSearch instance with the converted parameters and other configuration values.
        4. Calls the `run` method on the TabuSearch instance, which starts the algorithm execution.

        :return: None
        """
        # Wait for other processes to reach the barrier before starting
        self.start_barrier.wait()

        # Convert custom Python enum types to their corresponding C++ values
        initial_solution_method_cpp = map_initial_solution_method(self.config_params.initial_solution_method)
        neighbor_selection_method_cpp = map_neighbor_selection_method(self.config_params.neighbor_selection_method)
        tabu_list_limit_method_cpp = map_tabu_list_limit_method(self.config_params.tabu_list_limit_method)
        tenure_type_cpp = map_tenure_type(self.config_params.tenure_type)

        # Initialize the Tabu Search instance with algorithm parameters
        ts_instance = ts.TabuSearch(
            port=self.port,
            data_frequency_ms=self.data_frequency,
            dist_matrix=self.distance_matrix,
            duration_ms=self.config_params.duration_ms,
            initial_solution_method=initial_solution_method_cpp,
            neighbor_selection_method=neighbor_selection_method_cpp,
            max_neighbors=self.config_params.max_neighbors,
            tabu_list_limit_method=tabu_list_limit_method_cpp,
            tabu_list_custom_limit=self.config_params.tabu_list_custom_limit,
            tenure_type=tenure_type_cpp,
            constant_tenure=self.config_params.constant_tenure,
            random_tenure_range=self.config_params.random_tenure_range
        )

        # Run the Tabu Search algorithm
        ts_instance.run()
