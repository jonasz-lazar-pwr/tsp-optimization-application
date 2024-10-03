# src/utils/interfaces/main_window_interface.py

from abc import ABC, abstractmethod


class MainWindowInterface(ABC):
    @abstractmethod
    def run_simulated_annealing(self) -> None:
        """Method for handling the execution of the Simulated Annealing algorithm."""
        pass

    @abstractmethod
    def select_directory(self) -> None:
        """Method for handling directory selection for TSP files."""
        pass

    @abstractmethod
    def update_current_solution(self, solution: list[float]) -> None:
        """Updates the label displaying the current solution."""
        pass

    @abstractmethod
    def update_result(self, result: float) -> None:
        """Updates the label displaying the final result."""
        pass
