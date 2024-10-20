# src/interfaces/backend/components/algorithm_manager_interface.py

from abc import ABC, abstractmethod
from typing import Callable


class AlgorithmManagerInterface(ABC):
    @abstractmethod
    def start(self) -> None:
        """
        Starts the algorithm and receiver processes.
        """
        pass

    @abstractmethod
    def check_queue(self, handle_data_callback: Callable) -> None:
        """
        Checks the queue for new data and processes it using a callback function.
        """
        pass

    @abstractmethod
    def terminate_processes(self) -> None:
        """
        Terminates the receiver and main algorithm processes.
        """
        pass

    @abstractmethod
    def parse_message(self, data: str) -> tuple[int, int, list[int]]:
        """
        Parses the incoming data message.
        """
        pass