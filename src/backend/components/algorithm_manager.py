# src/backend/components/algorithm_manager.py

from typing import Optional, Type, Callable
from multiprocessing import Queue, Process, Barrier
from src.backend.components.processes.algorithm_process import AlgorithmProcess
from src.interfaces.backend.components import AlgorithmManagerInterface


class AlgorithmManager(AlgorithmManagerInterface):
    def __init__(self, algorithm_process_class: Type[AlgorithmProcess], distance_matrix: list[list[int]],
                 start_barrier: Barrier, port: int) -> None:
        """
        Initializes the manager (handler) for an algorithm process.

        :param algorithm_process_class: The class used to create the algorithm process.
        :param distance_matrix: The distance matrix for the TSP problem.
        :param start_barrier: The barrier to synchronize the start of processes.
        :param port: The port used for NNG socket communication between processes.
        :return: None
        """
        self.queue = Queue()
        self.algorithm_process_instance = algorithm_process_class(distance_matrix, self.queue, start_barrier, port)
        self.receiver_process: Optional[Process] = None
        self.algorithm_process: Optional[Process] = None
        self.is_receiving = False
        self.port = port

    def start(self) -> None:
        """
        Starts the algorithm and receiver processes.

        :return: None
        """
        self.receiver_process, self.algorithm_process = self.algorithm_process_instance.start()
        self.is_receiving = True

    def check_queue(self, handle_data_callback: Callable) -> None:
        """
        Checks the queue for new data and processes it using a callback function.

        :param handle_data_callback: The callback function to handle the data.
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
        Terminates the receiver and main algorithm processes.

        :return: None
        """
        if self.receiver_process and self.receiver_process.is_alive():
            self.receiver_process.terminate()
        if self.algorithm_process and self.algorithm_process.is_alive():
            self.algorithm_process.terminate()

    def parse_message(self, data: str) -> tuple[int, int, list[int]]:
        """
        Parses the incoming data message.

        :param data: The data string containing elapsed time, current cost, and current solution.
        :return: A tuple containing the elapsed time, current cost, and current solution.
        """
        try:
            parts = data.split(' ', 2)
            elapsed_time = int(parts[0])
            current_cost = int(parts[1])
            current_solution = list(map(int, parts[2].split(',')))
            return elapsed_time, current_cost, current_solution
        except (ValueError, IndexError) as e:
            print(f"Error parsing message: {data}, {e}")
            return 0, 0, []
