# src/backend/components/processes/algorithms_process.py

import time
import pynng

from typing import Optional
from multiprocessing import Process, Queue, Barrier
from src.interfaces.backend.components.processes.algorithm_process_interface import AlgorithmProcessInterface


class AlgorithmProcess(AlgorithmProcessInterface):
    def __init__(self, distance_matrix: list[list[int]], queue: Queue, start_barrier: Barrier, port: int) -> None:
        """
        Initializes the AlgorithmProcess class with the distance matrix, queue, start barrier, and port.

        :param distance_matrix: The distance matrix for the TSP problem.
        :param queue: The queue for data communication between processes.
        :param start_barrier: The barrier to synchronize the start of processes.
        :param port: The port used for NNG socket communication between processes.
        :return: None
        """
        self.distance_matrix = distance_matrix
        self.queue = queue
        self.start_barrier = start_barrier
        self.port = port

    def start(self) -> tuple[Process, Process]:
        """
        Starts the algorithm process and the receiver process.

        :return: Tuple of the receiver and algorithm processes.
        """
        receiver_process = Process(target=self.receive_data)
        receiver_process.start()

        time.sleep(1)

        algorithm_process = Process(target=self.run_algorithm)
        algorithm_process.start()

        return receiver_process, algorithm_process

    def setup_socket(self) -> Optional[pynng.Pair1]:
        """
        Sets up the NNG socket for communication.

        :return: An NNG socket object if the setup is successful, otherwise None.
        """
        try:
            sock = pynng.Pair1()
            sock.listen(f'tcp://127.0.0.1:{self.port}')
            return sock
        except pynng.AddressInUse:
            print(f"Address already in use on port {self.port}.")
        except pynng.NNGException as e:
            print(f"Failed to open NNG socket on port {self.port}: {e}")
        return None

    def receive_data(self) -> None:
        """
        Receives data from the algorithm process through the socket.

        :return: None
        """
        try:
            with self.setup_socket() as sock:
                while True:
                    try:
                        msg = sock.recv()
                        message = msg.decode()
                        if message == 'EOF':
                            self.queue.put('EOF')
                            break
                        self.queue.put(message)
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        break
        except Exception as e:
            print(f"Failed to set up NNG socket on port {self.port}: {e}")

    def run_algorithm(self) -> None:
        """
        Runs the algorithm (to be implemented by subclasses).

        :return: None
        """
        raise NotImplementedError("Subclasses should implement this method.")
