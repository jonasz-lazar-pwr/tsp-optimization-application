# src/interfaces/backend/components/processes/algorithm_process_interface.py

from abc import ABC, abstractmethod
from typing import Optional
from multiprocessing import Process
import pynng


class AlgorithmProcessInterface(ABC):
    @abstractmethod
    def start(self) -> tuple[Process, Process]:
        """
        Starts the algorithm process and the receiver process.
        """
        pass

    @abstractmethod
    def setup_socket(self) -> Optional[pynng.Pair1]:
        """
        Sets up the NNG socket for communication.
        """
        pass

    @abstractmethod
    def receive_data(self) -> None:
        """
        Receives data from the algorithm process through the socket.
        """
        pass

    @abstractmethod
    def run_algorithm(self) -> None:
        """
        Runs the algorithm (to be implemented by subclasses).
        """
        pass