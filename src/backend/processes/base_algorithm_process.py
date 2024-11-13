# src/backend/processes/algorithms_process.py

import time
import pynng
from typing import Optional
from multiprocessing import Process, Queue, Barrier


class BaseAlgorithmProcess:
    def __init__(self, port: int, data_frequency: int, distance_matrix: list[list[int]],
                 queue: Queue, start_barrier: Barrier, config_params) -> None:
        """
        Initializes the BaseAlgorithmProcess class, setting up communication ports, data frequency, and synchronization.

        :param port: The port used for NNG socket communication between processes.
        :param data_frequency: Frequency (in ms) for data updates.
        :param distance_matrix: Distance matrix for the TSP problem.
        :param queue: Queue for inter-process communication.
        :param start_barrier: Barrier for synchronizing start of algorithm processes.
        :param config_params: Configuration parameters for the algorithm.
        :return: None
        """
        self.port: int = port
        self.data_frequency: int = data_frequency
        self.distance_matrix: list[list[int]] = distance_matrix
        self.queue: Queue = queue
        self.start_barrier: Barrier = start_barrier
        self.config_params = config_params

    def start(self) -> tuple[Process, Process]:
        """
        Starts two separate processes: one for receiving data, and one for running the algorithm.

        :return: A tuple containing the receiver and algorithm processes.
        """
        # Creating a process for receiving data and starting it
        receiver_process = Process(target=self.receive_data)
        receiver_process.start()

        # Synchronizing the start of the algorithm process
        time.sleep(1)

        # Creating a process for running the algorithm and starting it
        algorithm_process = Process(target=self.run_algorithm)
        algorithm_process.start()

        return receiver_process, algorithm_process

    def setup_socket(self) -> Optional[pynng.Pair1]:
        """
        Configures an NNG socket for inter-process communication over the specified port.

        :return: NNG socket object if successfully set up, otherwise None.
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
        Receives data messages from the algorithm through the configured socket and places them in the queue.

        :return: None
        """
        try:
            # Initializing the NNG socket
            with self.setup_socket() as sock:
                while True:
                    try:
                        # Receiving a message from the algorithm
                        msg = sock.recv()
                        message = msg.decode()
                        if message == 'EOF':
                            self.queue.put('EOF')
                            break
                        # Placing the message in the queue
                        self.queue.put(message)
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        break
        except Exception as e:
            print(f"Failed to set up NNG socket on port {self.port}: {e}")

    def run_algorithm(self) -> None:
        """
        Placeholder for running the algorithm process. This method should be implemented by subclasses to define
        the specific algorithm logic.

        :return: None
        :raises NotImplementedError: Indicates that subclasses need to implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")
