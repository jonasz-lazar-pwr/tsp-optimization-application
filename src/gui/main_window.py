# src/gui/main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFrame, QVBoxLayout

from src.backend.configs.algorithm_config import AlgorithmConfig
from src.backend.task_manager import TaskManager
from src.gui.panels.management_panel import ManagementPanel
from src.gui.panels.results_panel import ResultsPanel
from src.gui.panels.visualization_panel import VisualizationPanel
from src.gui.dialogs.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self, task_manager: TaskManager) -> None:
        """
        Initializes the main window for the TSP Optimization Application.

        :param task_manager: An instance of TaskManager that handles algorithm operations.
        :return: None
        """
        super().__init__()
        self.setWindowTitle("TSP Optimization Application")

        self.file_loaded: bool = False  # Flag indicating if a TSP file has been loaded

        # Initialize TaskManager and SettingsDialog
        self.task_manager: TaskManager = task_manager
        self.settings_dialog: SettingsDialog = SettingsDialog(self)

        # Set up main layout with panels for management, visualization, and results
        self.main_layout: QHBoxLayout = QHBoxLayout()

        # Set up the management panel
        self.management_panel: ManagementPanel = ManagementPanel(self.task_manager, self.settings_dialog)
        self.management_panel.main_window = self

        management_frame = self.create_styled_frame(self.management_panel)

        # Right-side layout for visualization and results panels
        self.right_layout: QVBoxLayout = QVBoxLayout()

        # Set up visualization panel
        self.visualization_panel: VisualizationPanel = VisualizationPanel()
        self.visualization_panel.set_all_plots_visible(False)
        visualization_frame = self.create_styled_frame(self.visualization_panel)
        self.right_layout.addWidget(visualization_frame)

        # Set up results panel
        self.results_panel: ResultsPanel = ResultsPanel()
        results_frame = self.create_styled_frame(self.results_panel)
        results_frame.setFixedHeight(160)  # Adjust the height as needed
        self.right_layout.addWidget(results_frame)

        # Set up layout structure
        self.update_results_visibility(1)
        self.main_layout.addWidget(management_frame)
        self.main_layout.addLayout(self.right_layout)

        # Set stretch factors for main layout
        self.main_layout.setStretch(0, 1)  # Less space for management
        self.main_layout.setStretch(1, 3)  # More space for visualization and results

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Configure window display
        self.showMaximized()  # Expand window to full screen

        # Signal connections
        self.setup_signals()

    @staticmethod
    def create_styled_frame(widget: QWidget) -> QFrame:
        """
        Creates and styles a frame to wrap around the given widget.

        :param widget: The widget to be wrapped in the styled frame.
        :return: A styled QFrame containing the widget.
        """
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame { 
                background-color: #393939; 
                border: 1px solid #424242; 
                border-radius: 4px; 
            }
        """)
        layout = QVBoxLayout(frame)
        layout.addWidget(widget)
        return frame

    def setup_signals(self) -> None:
        """
        Sets up connections between signals and corresponding slot methods.
        Links actions in ManagementPanel and TaskManager with updates in the main GUI.

        :return: None
        """
        # Connect file selection signal from TSPInstancesWidget to load_selected_file
        self.management_panel.tsp_instances_widget.file_selected.connect(self.load_selected_file)

        # Connect the run algorithm signal from ManagementPanel to run_algorithm
        self.management_panel.run_algorithm_signal.connect(self.run_algorithm)

        # Connect tab changes in ManagementPanel to plot and result visibility updates
        self.management_panel.tab_changed.connect(self.update_plot_visibility_based_on_tab)
        self.management_panel.tab_changed.connect(self.update_results_visibility)

        # Connect TaskManager data signals to visualization and result update slots
        self.task_manager.current_data_signal_sa.connect(self.update_results_sa)
        self.task_manager.current_data_signal_ts.connect(self.update_results_ts)

    def load_selected_file(self, file_name: str) -> None:
        """
        Loads the selected TSP file and updates the visualization and result panels accordingly.

        :param file_name: The name of the selected TSP file.
        :return: None
        """
        # Retrieve the TSP file metadata from the catalog
        tsp_file = self.task_manager.catalog.get_file_by_name(file_name)
        if tsp_file:
            # Set the file_loaded flag to indicate that a file has been successfully loaded
            self.file_loaded = True

            # Hide all plots and clear previous data in visualization and results panels
            self.visualization_panel.set_all_plots_visible(False)
            self.visualization_panel.clear_plots()
            self.results_panel.clear_results()

            # Check if the file includes coordinates for city mapping
            has_coordinates = bool(tsp_file.coordinates or tsp_file.display_coordinates)
            if has_coordinates:
                # Extract and update the city map data in the visualization panel
                coordinates = tsp_file.coordinates or tsp_file.display_coordinates
                self.visualization_panel.update_city_map_data(coordinates)

            # Set the optimal cost in the results panel for both SA and TS
            optimal_cost = tsp_file.optimal_result
            self.results_panel.set_optimal_cost(optimal_cost, "SA")
            self.results_panel.set_optimal_cost(optimal_cost, "TS")

            # Update the visibility of plots based on the currently selected tab in ManagementPanel
            tab_index = self.management_panel.algorithm_tab_widget.currentIndex()
            self.update_plot_visibility_based_on_tab(tab_index)

    def update_plot_visibility_based_on_tab(self, tab_index: int) -> None:
        """
        Updates the visibility of plots based on the selected tab and the availability of coordinates in the loaded file.

        :param tab_index: Index of the selected tab.
        :return: None
        """
        # If no file is loaded, hide all plots and return immediately
        if not self.file_loaded:
            self.visualization_panel.set_all_plots_visible(False)
            return

        # Check if coordinates are available for the loaded file
        has_coordinates = any([
            self.visualization_panel.city_plot_widget_sa.coordinates,
            self.visualization_panel.city_plot_widget_ts.coordinates
        ])

        # Adjust layout based on selected tab and coordinate availability
        self.visualization_panel.adjust_layout(tab_index, has_coordinates)

    def update_results_visibility(self, tab_index: int) -> None:
        """
        Updates the visibility of result panels based on the selected tab.

        :param tab_index: Index of the selected tab.
        :return: None
        """
        # Determine which result panels to display based on the tab selection
        if tab_index == 0:  # SA only
            self.results_panel.update_visibility(show_sa=True, show_ts=False)
        elif tab_index == 1:  # SA + TS
            self.results_panel.update_visibility(show_sa=True, show_ts=True)
        elif tab_index == 2:  # TS only
            self.results_panel.update_visibility(show_sa=False, show_ts=True)

    def run_algorithm(self, config: AlgorithmConfig) -> None:
        """
        Starts the specified algorithm(s) with the provided parameters.

        :param config: The configuration object containing algorithm parameters.
        :return: None
        """
        # Clear previous plots and results before starting a new algorithm run
        self.visualization_panel.clear_plots_partially()
        self.results_panel.clear_results_partially()

        # Start the algorithm(s) with the given configuration
        self.task_manager.start_algorithm_for_file(config)

    def update_results_sa(self, elapsed_time: int, best_cost: int, current_cost: int,
                          current_solution: list[int]) -> None:
        """
        Updates the results and plots for the Simulated Annealing (SA) algorithm.

        :param elapsed_time: Time elapsed since the start of the SA algorithm.
        :param best_cost: Best cost found so far by the SA algorithm.
        :param current_cost: Current cost at this iteration of the SA algorithm.
        :param current_solution: Current solution path as a list of city indices.
        :return: None
        """
        # Update the SA results and plot with the new data
        self.results_panel.update_sa_results(best_cost, current_cost)
        self.visualization_panel.update_sa_plots(elapsed_time, current_cost, current_solution)

    def update_results_ts(self, elapsed_time: int, best_cost: int, current_cost: int,
                          current_solution: list[int]) -> None:
        """
        Updates the results and plots for the Tabu Search (TS) algorithm.

        :param elapsed_time: Time elapsed since the start of the TS algorithm.
        :param best_cost: Best cost found so far by the TS algorithm.
        :param current_cost: Current cost at this iteration of the TS algorithm.
        :param current_solution: Current solution path as a list of city indices.
        :return: None
        """
        # Update the TS results and plot with the new data
        self.results_panel.update_ts_results(best_cost, current_cost)
        self.visualization_panel.update_ts_plots(elapsed_time, current_cost, current_solution)
