# src/backend/task_manager.py

from typing import Dict
from PySide6.QtCore import QObject, Signal, QTimer
from multiprocessing import Barrier

from src.backend.components.report_directory_selector import ReportDirectorySelector
from src.backend.components.report_generator import ReportGenerator
from src.backend.components.tsp_directory_selector import TSPDirectorySelector
from src.backend.components.algorithm_manager import AlgorithmManager
from src.backend.configs.algorithm_config import AlgorithmConfig
from src.backend.processes.simulated_annealing_process import SimulatedAnnealingProcess
from src.backend.processes.tabu_search_process import TabuSearchProcess
from src.backend.tsp_management.tsp_catalog import TSPCatalog


class TaskManager(QObject):
    # Signal emitted when new data is available for the SA algorithm
    current_data_signal_sa: Signal = Signal(int, int, int, list)
    # Signal emitted when new data is available for the TS algorithm
    current_data_signal_ts: Signal = Signal(int, int, int, list)
    # Signal emitted when the SA algorithm finishes
    sa_finished_signal: Signal = Signal()
    # Signal emitted when the TS algorithm finishes
    ts_finished_signal: Signal = Signal()

    def __init__(self) -> None:
        """
        Initializes the TaskManager class with the TSP catalog, selectors, and algorithm manager dictionary.

        :return: None
        """
        super().__init__()
        self.catalog: TSPCatalog = TSPCatalog("data/metadata/optimal_results.json")
        self.directory_selector: TSPDirectorySelector = TSPDirectorySelector(self.catalog)
        self.report_selector: ReportDirectorySelector = ReportDirectorySelector("data/reports")
        self.algorithms_manager_dict: Dict[str, AlgorithmManager] = {}

    def select_tsp_directory(self) -> None:
        """
        Invokes TSPDirectorySelector to select a directory and automatically load TSP files.

        :return: None
        """
        self.directory_selector.select_directory_and_load_files()

    def get_files_data_for_table(self) -> list[tuple[str, str, str]]:
        """
        Returns a list of tuples with file names, dimensions, edge weight type, and coordinates presence.

        :return: List of tuples (name, dimension, edge_weight_type, has_coordinates).
        """
        return [
            (
                file.name,
                str(file.dimension),
                "Yes" if file.coordinates or file.display_coordinates else "No"
            )
            for file in self.catalog.tsp_files
        ]

    def start_algorithm_for_file(self, config: AlgorithmConfig) -> None:
        """
        Launches processes for the selected algorithm(s) on a given TSP file.

        :param config: The configuration object containing algorithm parameters.
        :return: None
        """
        num_algorithms: int = len(config.algorithms)
        start_barrier: Barrier = Barrier(num_algorithms)

        tsp_file = self.catalog.get_file_by_name(config.file_name)
        if tsp_file:
            if not tsp_file.has_loaded:
                tsp_file.load_distance_matrix()

            distance_matrix = tsp_file.get_distance_matrix()
            if distance_matrix:
                self.algorithms_manager_dict = {}
                for algorithm_name in config.algorithms:
                    if algorithm_name == "SA" and config.sa_params:
                        self.algorithms_manager_dict["SA"] = AlgorithmManager(
                            SimulatedAnnealingProcess,
                            config.sa_port,
                            config.data_frequency,
                            distance_matrix,
                            start_barrier,
                            config.sa_params
                        )
                        self.algorithms_manager_dict["SA"].start()
                        self._check_queue_sa(config.data_frequency)

                    elif algorithm_name == "TS" and config.ts_params:
                        self.algorithms_manager_dict["TS"] = AlgorithmManager(
                            TabuSearchProcess,
                            config.ts_port,
                            config.data_frequency,
                            distance_matrix,
                            start_barrier,
                            config.ts_params
                        )
                        self.algorithms_manager_dict["TS"].start()
                        self._check_queue_ts(config.data_frequency)
                    else:
                        print(f"Algorithm {algorithm_name} not recognized.")
            else:
                print("Distance matrix not available.")
        else:
            print("Selected file not found.")

    def _check_queue_sa(self, frequency: int) -> None:
        """
        Periodically checks the data queue for the SA algorithm.

        :param frequency: Update frequency in milliseconds.
        :return: None
        """
        try:
            if "SA" in self.algorithms_manager_dict:
                algorithm_manager = self.algorithms_manager_dict["SA"]
                algorithm_manager.check_queue(lambda data: self._handle_data_sa(data))
        finally:
            if "SA" in self.algorithms_manager_dict and not self.algorithms_manager_dict["SA"].is_receiving:
                self.sa_finished_signal.emit()
            else:
                QTimer.singleShot(frequency, lambda: self._check_queue_sa(frequency))

    def _check_queue_ts(self, frequency: int) -> None:
        """
        Periodically checks the data queue for the TS algorithm.

        :param frequency: Update frequency in milliseconds.
        :return: None
        """
        try:
            if "TS" in self.algorithms_manager_dict:
                algorithm_manager = self.algorithms_manager_dict["TS"]
                algorithm_manager.check_queue(lambda data: self._handle_data_ts(data))
        finally:
            if "TS" in self.algorithms_manager_dict and not self.algorithms_manager_dict["TS"].is_receiving:
                self.ts_finished_signal.emit()
            else:
                QTimer.singleShot(frequency, lambda: self._check_queue_ts(frequency))

    def _handle_data_sa(self, data: str) -> None:
        """
        Handles data received from the SA algorithm and emits a signal for the GUI.

        :param data: Data string received from SA.
        :return: None
        """
        elapsed_time, best_cost, current_cost, current_solution = self.algorithms_manager_dict["SA"].parse_message(data)

        if elapsed_time == 0 and current_cost == 0 and best_cost == 0 and not current_solution:
            print("Received invalid data for SA. Skipping update.")
            return
        self.current_data_signal_sa.emit(elapsed_time, best_cost, current_cost, current_solution)

    def _handle_data_ts(self, data: str) -> None:
        """
        Handles data received from the TS algorithm and emits a signal for the GUI.

        :param data: Data string received from TS.
        :return: None
        """
        elapsed_time, best_cost, current_cost, current_solution = self.algorithms_manager_dict["TS"].parse_message(data)

        if elapsed_time == 0 and current_cost == 0 and best_cost == 0 and not current_solution:
            print("Received invalid data for TS. Skipping update.")
            return
        self.current_data_signal_ts.emit(elapsed_time, best_cost, current_cost, current_solution)

    def stop_algorithms(self) -> None:
        """
        Stops all running algorithms and clears the algorithm manager dictionary.

        :return: None
        """
        for algorithm_name, manager in self.algorithms_manager_dict.items():
            manager.terminate_processes()
            if algorithm_name == "SA":
                self.sa_finished_signal.emit()
            elif algorithm_name == "TS":
                self.ts_finished_signal.emit()
        self.algorithms_manager_dict.clear()

    def get_instance_data(self, file_name: str) -> dict:
        """
        Retrieves detailed information about a TSP instance.

        :param file_name: Name of the TSP file.
        :return: Dictionary containing instance details.
        """
        tsp_file = self.catalog.get_file_by_name(file_name)
        if tsp_file:
            return {
                "name": tsp_file.name,
                "dimension": tsp_file.dimension,
                "edge_weight_type": tsp_file.edge_weight_type,
                "optimal_length": tsp_file.optimal_result,
                "coordinates": tsp_file.coordinates or tsp_file.display_coordinates
            }
        else:
            print(f"File {file_name} not found in catalog.")
            return {}

    def generate_report(self, file_name: str, instance_data: dict, algorithm_results: dict, plots: dict) -> None:
        """
        Generates a report using the specified data and saves it to the chosen path.

        :param file_name: Name of the TSP instance.
        :param instance_data: Dictionary containing instance data.
        :param algorithm_results: Dictionary with algorithm results.
        :param plots: Dictionary of plot data.
        :return: None
        """
        default_report_name = self.report_selector.generate_default_report_name(file_name)
        save_path = self.report_selector.select_report_path(default_report_name)

        if not save_path:
            print("Report generation canceled.")
            return

        report_generator = ReportGenerator(
            instance_name=instance_data["name"],
            instance_data=instance_data,
            algorithm_results=algorithm_results,
            plots=plots,
            output_path=save_path
        )
        report_generator.generate_report()
