# src/backend/components/processes/simulated_annealing_process.py

import compiled_binaries.tsp_sa as sa
from multiprocessing import Queue, Barrier
from src.backend.components.processes.algorithm_process import AlgorithmProcess


class SimulatedAnnealingProcess(AlgorithmProcess):
    def __init__(self, distance_matrix: list[list[int]], queue: Queue, start_barrier: Barrier, port: int) -> None:
        """
        Initializes the SimulatedAnnealingProcess with the distance matrix, queue, start barrier, and port.

        :param distance_matrix: The distance matrix for the TSP problem.
        :param queue: The queue for data communication between processes.
        :param start_barrier: The barrier to synchronize the start of processes.
        :param port: The port used for NNG socket communication between processes.
        :return: None
        """
        super().__init__(distance_matrix, queue, start_barrier, port)

    def run_algorithm(self) -> None:
        """
        Runs the Simulated Annealing algorithm.

        :return: None
        """
        # Wait for other processes to reach the barrier before starting
        self.start_barrier.wait()

        # Initialize the Simulated Annealing instance with algorithm parameters
        sa_instance = sa.SimulatedAnnealing(
            duration_ms=1000,
            port=self.port,
            dist_matrix=self.distance_matrix,
            initial_temp_type=sa.InitialTempType.SAMPLING,
            temp_decay_type=sa.TempDecayType.GEO,
            alpha=0.99,
            beta=0.1,
            steps_per_temp=2000,
            move_type=sa.MoveType.INSERT,
            initial_solution_type=sa.InitialSolutionType.RANDOM
        )

        # Run the Simulated Annealing algorithm
        sa_instance.run()