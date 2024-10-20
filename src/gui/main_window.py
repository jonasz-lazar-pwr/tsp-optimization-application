# src/gui/main_window.py

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QListView

from src.backend.task_manager import TaskManager
from src.gui.components.plots.cost_plot_widget import CostPlotWidget
from src.gui.components.plots.city_map_widget import CityMapWidget


class MainWindow(QMainWindow):
    def __init__(self, task_manager: TaskManager) -> None:
        """
        Initializes the main application window.

        :param task_manager: An instance of TaskManager responsible for managing tasks.
        """
        super().__init__()
        self.setWindowTitle("TSP Optimization Application")

        # Inicjalizacja TaskManager
        self.task_manager = task_manager

        # Podłączenie sygnałów TaskManagera do aktualizacji GUI
        self.task_manager.current_data_signal_sa.connect(self.update_simulation_data_sa)
        self.task_manager.current_data_signal_ts.connect(self.update_simulation_data_ts)

        # Layout setup
        self.layout = QVBoxLayout()

        # Użycie QListView
        self.file_list_view = QListView()
        self.file_list_view.setModel(QStandardItemModel())
        self.file_list_view.selectionModel().selectionChanged.connect(self.on_file_selection_change)
        self.layout.addWidget(self.file_list_view)

        # Button to run the Simulated Annealing algorithm
        self.run_button_sa = QPushButton("Run SA")
        self.run_button_sa.clicked.connect(lambda: self.run_single_algorithm("SA"))
        self.layout.addWidget(self.run_button_sa)

        # Button to run the Tabu Search algorithm
        self.run_button_ts = QPushButton("Run TS")
        self.run_button_ts.clicked.connect(lambda: self.run_single_algorithm("TS"))
        self.layout.addWidget(self.run_button_ts)

        # Button to run both algorithms
        self.run_button_all = QPushButton("Run Both")
        self.run_button_all.clicked.connect(self.run_both_algorithms)
        self.layout.addWidget(self.run_button_all)

        # Button to select a directory with TSP files
        self.select_directory_button = QPushButton("Select TSP Directory")
        self.select_directory_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_directory_button)

        # Button to clear the plots
        self.clear_button = QPushButton("Clear Plots")
        self.clear_button.clicked.connect(self.clear_plots_partial)
        self.clear_button.setVisible(False)  # Hide the button
        self.layout.addWidget(self.clear_button)

        # Plot to display the cost function value over time for Simulated Annealing
        self.cost_plot_widget_sa = CostPlotWidget(self)
        self.cost_plot_widget_sa.setVisible(False)  # Hide the plot on start
        self.layout.addWidget(self.cost_plot_widget_sa)

        # Plot to display the route on the map for Simulated Annealing
        self.city_map_widget_sa = CityMapWidget(self)
        self.city_map_widget_sa.setVisible(False)  # Hide the plot on start
        self.layout.addWidget(self.city_map_widget_sa)

        # Plot to display the cost function value over time for Tabu Search
        self.cost_plot_widget_ts = CostPlotWidget(self)
        self.cost_plot_widget_ts.setVisible(False)  # Hide the plot on start
        self.layout.addWidget(self.cost_plot_widget_ts)

        # Plot to display the route on the map for Tabu Search
        self.city_map_widget_ts = CityMapWidget(self)
        self.city_map_widget_ts.setVisible(False)  # Hide the plot on start
        self.layout.addWidget(self.city_map_widget_ts)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def select_directory(self) -> None:
        """
        Handles the directory selection and file loading.
        """
        self.task_manager.select_tsp_directory()
        self.update_file_list()

    def update_file_list(self) -> None:
        """
        Updates the file selector with loaded TSP file names.
        """
        model = self.file_list_view.model()
        model.clear()  # Wyczyść poprzednie elementy

        file_names = self.task_manager.get_loaded_file_names()
        for file_name in file_names:
            item = QStandardItem(file_name)
            model.appendRow(item)

    def on_file_selection_change(self) -> None:
        selected_indexes = self.file_list_view.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_file_name = selected_indexes[0].data()
            self.load_selected_file(selected_file_name)

    def load_selected_file(self, file_name: str) -> None:
        tsp_file = self.task_manager.catalog.get_file_by_name(file_name)
        if tsp_file:
            self.clear_button.setVisible(False)

            self.cost_plot_widget_sa.setVisible(False)
            self.city_map_widget_sa.setVisible(False)

            self.cost_plot_widget_ts.setVisible(False)
            self.city_map_widget_ts.setVisible(False)

            if tsp_file.coordinates or tsp_file.display_coordinates:
                self.clear_plots_all()
                self.city_map_widget_sa.coordinates = tsp_file.coordinates or tsp_file.display_coordinates
                self.city_map_widget_sa.set_city_positions()
                self.city_map_widget_sa.setVisible(True)

                self.city_map_widget_ts.coordinates = tsp_file.coordinates or tsp_file.display_coordinates
                self.city_map_widget_ts.set_city_positions()
                self.city_map_widget_ts.setVisible(True)

            self.cost_plot_widget_sa.setVisible(True)
            self.cost_plot_widget_ts.setVisible(True)
            self.clear_button.setVisible(True)

    def run_both_algorithms(self) -> None:
        """
        Handles starting both SA and TS algorithms for the selected file.
        """
        selected_indexes = self.file_list_view.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_file_name = selected_indexes[0].data()
            if selected_file_name:
                self.clear_plots_partial()
                # Przekazujemy konfigurację "SA + TS" i listę ["SA", "TS"]
                self.task_manager.start_algorithm_for_file(["SA", "TS"], selected_file_name)

    def run_single_algorithm(self, algorithm_name: str) -> None:
        """
        Handles starting a single algorithm for the selected file.
        """
        selected_indexes = self.file_list_view.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_file_name = selected_indexes[0].data()
            if selected_file_name:
                self.clear_plots_partial()
                # Przekazujemy konfigurację algorytmu ("SA" lub "TS") i odpowiednią listę
                self.task_manager.start_algorithm_for_file([algorithm_name], selected_file_name)

    def update_simulation_data(self, algorithm_name: str, elapsed_time: int, current_cost: int,
                               current_solution: list[int]) -> None:
        """
        Updates the plot and label displaying the current cost, elapsed time, and the current solution (route) for the given algorithm.

        :param algorithm_name: The name of the algorithm ("SA" or "TS").
        :param elapsed_time: The current elapsed time in milliseconds.
        :param current_cost: The current cost (objective function value).
        :param current_solution: The current solution (list of cities in the current route).
        """
        if algorithm_name == "SA":
            # Aktualizacja dla SA
            if self.cost_plot_widget_sa.isVisible():
                self.cost_plot_widget_sa.update_plot(elapsed_time, current_cost)
            if self.city_map_widget_sa.isVisible():
                self.city_map_widget_sa.update_route(current_solution)
        elif algorithm_name == "TS":
            # Aktualizacja dla TS
            if self.cost_plot_widget_ts.isVisible():
                self.cost_plot_widget_ts.update_plot(elapsed_time, current_cost)
            if self.city_map_widget_ts.isVisible():
                self.city_map_widget_ts.update_route(current_solution)

    def update_simulation_data_sa(self, elapsed_time: int, current_cost: int, current_solution: list[int]) -> None:
        """
        Updates the plot and label displaying the current cost, elapsed time, and the current solution (route).

        :param elapsed_time: The current elapsed time in milliseconds.
        :param current_cost: The current cost (objective function value).
        :param current_solution: The current solution (list of cities in the current route).
        """
        # Aktualizacja wykresu kosztów w czasie, jeśli widoczny
        if self.cost_plot_widget_sa.isVisible():
            self.cost_plot_widget_sa.update_plot(elapsed_time, current_cost)

        # Aktualizacja trasy (permutacja miast) na mapie, jeśli widoczny
        if self.city_map_widget_sa.isVisible():
            self.city_map_widget_sa.update_route(current_solution)

    def update_simulation_data_ts(self, elapsed_time: int, current_cost: int, current_solution: list[int]) -> None:
        """
        Updates the plot and label displaying the current cost, elapsed time, and the current solution (route) for TS.

        :param elapsed_time: The current elapsed time in milliseconds.
        :param current_cost: The current cost (objective function value).
        :param current_solution: The current solution (list of cities in the current route).
        """
        # Aktualizacja wykresu kosztów dla Tabu Search, jeśli widoczny
        if self.cost_plot_widget_ts.isVisible():
            self.cost_plot_widget_ts.update_plot(elapsed_time, current_cost)

        # Aktualizacja trasy na mapie dla Tabu Search, jeśli widoczny
        if self.city_map_widget_ts.isVisible():
            self.city_map_widget_ts.update_route(current_solution)

    def clear_plots_all(self) -> None:
        """
        Czyści wszystkie wykresy (koszt, koordynaty oraz trasa miast).
        """
        self.cost_plot_widget_sa.clear()
        self.city_map_widget_sa.clear_all()
        self.cost_plot_widget_ts.clear()
        self.city_map_widget_ts.clear_all()

    def clear_plots_partial(self) -> None:
        """
        Czyści wykresy częściowo (koszt oraz trasa miast).
        """
        self.cost_plot_widget_sa.clear()
        self.city_map_widget_sa.clear_route()
        self.cost_plot_widget_ts.clear()
        self.city_map_widget_ts.clear_route()
