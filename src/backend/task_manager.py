# src/backend/task_manager.py

from typing import Optional
from PySide6.QtCore import QObject, Signal, QTimer
from multiprocessing import Barrier

from src.gui.components.directory_selector import DirectorySelector
from src.backend.components.algorithm_manager import AlgorithmManager
from src.backend.components.processes.simulated_annealing_process import SimulatedAnnealingProcess
from src.backend.components.processes.tabu_search_process import TabuSearchProcess
from src.backend.components.tsp_management.tsp_catalog import TSPCatalog


class TaskManager(QObject):
    current_data_signal_sa = Signal(int, int, list)
    current_data_signal_ts = Signal(int, int, list)

    def __init__(self) -> None:
        """
        Initializes the TaskManager class with the TSP catalog and the directory selector.

        :return: None
        """
        super().__init__()
        self.catalog = TSPCatalog("data/metadata/optimal_results.json")
        self.directory_selector = DirectorySelector(self.catalog)
        self.algorithms_manager_dict: Optional[dict[str, AlgorithmManager]] = None

    def select_tsp_directory(self) -> None:
        """
        Invokes DirectorySelector to select a directory and automatically load TSP files.

        :return: None
        """
        self.directory_selector.select_directory_and_load_files()

    def get_loaded_file_names(self) -> list[str]:
        """
        Retrieves the list of loaded TSP file names.

        :return: List of file names.
        """
        return [file.name for file in self.catalog.tsp_files]


    def start_algorithm_for_file(self, algorithms: list[str], file_name: str) -> None:
        """
        Starts the specified algorithm processes for the selected TSP file.

        :param algorithms: List of algorithm names to start (e.g., ["SA"] or ["SA", "TS"]).
        :param file_name: The name of the selected file.
        :return: None
        """
        num_algorithms = len(algorithms)
        start_barrier = Barrier(num_algorithms)

        tsp_file = self.catalog.get_file_by_name(file_name)
        if tsp_file:
            if not tsp_file.has_loaded:
                tsp_file.load_distance_matrix()

            distance_matrix = tsp_file.get_distance_matrix()
            if distance_matrix:
                self.algorithms_manager_dict = {}
                for algorithm_name in algorithms:
                    if algorithm_name == "SA":
                        self.algorithms_manager_dict["SA"] = AlgorithmManager(
                            SimulatedAnnealingProcess,
                            distance_matrix,
                            start_barrier,
                            5555
                        )
                        self.algorithms_manager_dict["SA"].start()
                        self._check_queue_sa()

                    elif algorithm_name == "TS":
                        self.algorithms_manager_dict["TS"] = AlgorithmManager(
                            TabuSearchProcess,
                            distance_matrix,
                            start_barrier,
                            6666
                        )
                        self.algorithms_manager_dict["TS"].start()
                        self._check_queue_ts()
                    else:
                        print(f"Algorithm {algorithm_name} not recognized.")
            else:
                print("Distance matrix not available.")
        else:
            print("Selected file not found.")

    def _check_queue_sa(self) -> None:
        """
        Regularly checks the queue for the SA algorithm.

        :return: None
        """
        try:
            algorithm_manager = self.algorithms_manager_dict["SA"]
            algorithm_manager.check_queue(lambda data: self._handle_data_sa(data))
        finally:
            if self.algorithms_manager_dict["SA"].is_receiving:
                QTimer.singleShot(1, self._check_queue_sa)

    def _check_queue_ts(self) -> None:
        """
        Regularly checks the queue for the TS algorithm.

        :return: None
        """
        try:
            algorithm_manager = self.algorithms_manager_dict["TS"]
            algorithm_manager.check_queue(lambda data: self._handle_data_ts(data))
        finally:
            if self.algorithms_manager_dict["TS"].is_receiving:
                QTimer.singleShot(1, self._check_queue_ts)

    def _handle_data_sa(self, data: str) -> None:
        """
        Handles data received from the SA algorithm.

        :param data: The data string received from the algorithm.
        :return: None
        """
        elapsed_time, current_cost, current_solution = self.algorithms_manager_dict["SA"].parse_message(data)

        if elapsed_time == 0 and current_cost == 0 and not current_solution:
            print("Received invalid data for SA. Skipping update.")
            return
        self.current_data_signal_sa.emit(elapsed_time, current_cost, current_solution)

    def _handle_data_ts(self, data: str) -> None:
        """
        Handles data received from the TS algorithm.

        :param data: The data string received from the algorithm.
        :return: None
        """
        elapsed_time, current_cost, current_solution = self.algorithms_manager_dict["TS"].parse_message(data)

        if elapsed_time == 0 and current_cost == 0 and not current_solution:
            print("Received invalid data for TS. Skipping update.")
            return
        self.current_data_signal_ts.emit(elapsed_time, current_cost, current_solution)
