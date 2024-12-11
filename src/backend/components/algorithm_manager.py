# src/backend/components/algorithm_manager.py

from typing import Optional, Type, Callable
from multiprocessing import Queue, Process, Barrier

from src.backend.processes.base_algorithm_process import BaseAlgorithmProcess


class AlgorithmManager:
    def __init__(self, algorithm_process_class: Type[BaseAlgorithmProcess], port: int, data_frequency: int,
                 distance_matrix: list[list[int]], start_barrier: Barrier, config_params) -> None:
        """
        Initializes the manager (handler) for an algorithm process, setting up required resources
        such as the inter-process communication queue, process instances, and synchronization barriers.

        :param algorithm_process_class: The class used to create the algorithm process.
        :param port: The communication port for socket communication.
        :param data_frequency: The frequency for data updates.
        :param distance_matrix: The distance matrix for the TSP problem.
        :param start_barrier: The barrier for synchronizing the start of processes.
        :param config_params: Configuration parameters for the algorithm.
        :return: None
        """
        self.queue: Queue = Queue()
        self.algorithm_process_instance: BaseAlgorithmProcess = algorithm_process_class(
            port, data_frequency, distance_matrix, self.queue, start_barrier, config_params
        )
        self.receiver_process: Optional[Process] = None
        self.algorithm_process: Optional[Process] = None
        self.is_receiving: bool = False

    def start(self) -> None:
        """
        Starts the algorithm and receiver processes, enabling data communication and processing.

        :return: None
        """
        self.receiver_process, self.algorithm_process = self.algorithm_process_instance.start()
        self.is_receiving = True

    def check_queue(self, handle_data_callback: Callable) -> None:
        """
        Checks the queue for new data messages and processes each message using a callback function.

        :param handle_data_callback: The callback function to handle the data received in the queue.
        :return: None
        """
        while not self.queue.empty():
            current_data = self.queue.get()
            if current_data == 'EOF':
                self.is_receiving = False
                self.terminate_processes()
                return
            handle_data_callback(current_data)

    def terminate_processes(self) -> None:
        """
        Terminates both the receiver and algorithm processes if they are active.

        :return: None
        """
        if self.receiver_process and self.receiver_process.is_alive():
            self.receiver_process.terminate()
        if self.algorithm_process and self.algorithm_process.is_alive():
            self.algorithm_process.terminate()

    def parse_message(self, data: str) -> tuple[int, int, int, list[int]]:
        """
        Parses an incoming data message string to extract algorithm metrics such as elapsed time,
        best cost, current cost, and the current solution route.

        :param data: The data string containing elapsed time, best cost, current cost, and current solution route.
        :return: A tuple containing the parsed values for elapsed time, best cost, current cost, and the current solution route.
        """
        try:
            parts = data.split(' ', 3)
            elapsed_time = int(parts[0])
            best_cost = int(parts[1])
            current_cost = int(parts[2])
            current_solution = list(map(int, parts[3].split(',')))
            return elapsed_time, best_cost, current_cost, current_solution
        except (ValueError, IndexError) as e:
            print(f"Error parsing message: {data}, {e}")
            return 0, 0, 0, []
