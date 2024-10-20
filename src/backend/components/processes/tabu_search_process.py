# src/backend/components/processes/tabu_search_process.py

import compiled_binaries.tsp_ts as ts
from multiprocessing import Queue, Barrier
from src.backend.components.processes.algorithm_process import AlgorithmProcess


class TabuSearchProcess(AlgorithmProcess):
    def __init__(self, distance_matrix: list[list[int]], queue: Queue, start_barrier: Barrier, port: int) -> None:
        """
        Initializes the TabuSearchProcess with the distance matrix, queue, start barrier, and port.

        :param distance_matrix: The distance matrix for the TSP problem.
        :param queue: The queue for data communication between processes.
        :param start_barrier: The barrier to synchronize the start of processes.
        :param port: The port used for NNG socket communication between processes.
        :return: None
        """
        super().__init__(distance_matrix, queue, start_barrier, port)

    def run_algorithm(self) -> None:
        """
        Runs the Tabu Search algorithm.

        :return: None
        """
        # Wait for other processes to reach the barrier before starting
        self.start_barrier.wait()

        # Initialize the Tabu Search instance with algorithm parameters
        ts_instance = ts.TabuSearch(
            duration_ms=1000,
            port=self.port,
            dist_matrix=self.distance_matrix,
            tenure=100,
            random_tenure_range=(10, 50),
            tenure_type=ts.TenureType.CONSTANT,
            limit_type=ts.TabuListLimitType.N,
            custom_limit=50,
            max_neighbors=50,
            move_type=ts.MoveType.SWAP,
            initial_solution_type=ts.InitialSolutionType.RANDOM
        )

        # Run the Tabu Search algorithm
        ts_instance.run()
