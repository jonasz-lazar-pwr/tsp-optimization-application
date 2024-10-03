# src/utils/interfaces/task_manager_interface.py

from abc import ABC, abstractmethod


class TaskManagerInterface(ABC):
    @abstractmethod
    def select_tsp_directory(self) -> None:
        """Invokes DirectorySelector to select a directory and automatically load TSP files."""
        pass

    @abstractmethod
    def load_tsp_files(self, directory_path: str) -> None:
        """Loads .tsp files from the selected directory using TSPCatalog."""
        pass

    @abstractmethod
    def start_simulated_annealing(self, distance_matrix: list[list[float]], temperature: float, iterations: int) -> None:
        """Starts the Simulated Annealing algorithm in a separate thread."""
        pass

    @abstractmethod
    def update_current_solution(self, solution: list[float]) -> None:
        """Method called by the thread when a new current solution is provided."""
        pass

    @abstractmethod
    def update_final_result(self, result: float) -> None:
        """Method called by the thread when the algorithm finishes and provides the final result."""
        pass

    @abstractmethod
    def stop_current_algorithm(self) -> None:
        """Stops the currently running algorithm."""
        pass
