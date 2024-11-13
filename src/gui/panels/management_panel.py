# src/gui/panels/management_panel.py

from typing import Optional, Any
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QHBoxLayout, QTabWidget

from src.backend.configs.algorithm_config import AlgorithmConfig
from src.gui.widgets.management.tsp_instances_widget import TSPInstancesWidget
from src.gui.widgets.management.algorithm_settings_widget import AlgorithmSettingsWidget
from src.backend.task_manager import TaskManager
from src.gui.dialogs.settings_dialog import SettingsDialog


class ManagementPanel(QWidget):
    # Signal emitted to start the algorithm with the selected parameters
    run_algorithm_signal = Signal(AlgorithmConfig)
    # Signal emitted when the tab changes, providing the new tab index.
    tab_changed = Signal(int)

    def __init__(self, task_manager: TaskManager, settings_dialog: SettingsDialog, main_window: Optional[Any] = None,
                 parent: Optional[QWidget] = None) -> None:
        """
        Initializes the ManagementPanel, setting up layout, buttons, stacked widgets, and connecting signals.

        :param task_manager: The TaskManager instance for managing algorithm operations.
        :param settings_dialog: The settings dialog for adjusting configuration.
        :param main_window: Reference to the MainWindow for accessing other GUI components.
        :param parent: Optional parent widget.
        :return: None
        """
        super().__init__(parent)
        self.task_manager: TaskManager = task_manager
        self.settings_dialog: SettingsDialog = settings_dialog
        self.main_window: Optional[Any] = main_window
        self.selected_file_name: Optional[str] = None  # Stores the selected TSP file name

        # Initialize the main layout and setup additional components
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # Set up layout and signals
        self.setup_layout()
        self.setup_signals()

    def setup_layout(self) -> None:
        """
        Configures the layout for the ManagementPanel, including buttons, tab widgets, and additional controls.

        :return: None
        """
        # Algorithm settings and TSP instances buttons
        self.algorithm_settings_button: QPushButton = QPushButton("Algorithm Settings")
        self.algorithm_settings_button.setEnabled(False)
        self.tsp_instances_button: QPushButton = QPushButton("TSP Instances")

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.algorithm_settings_button)
        button_layout.addWidget(self.tsp_instances_button)
        self.layout.addLayout(button_layout)

        # Stacked widget and tab configuration
        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.tsp_instances_widget: TSPInstancesWidget = TSPInstancesWidget(self.task_manager)
        self.algorithm_tab_widget: QTabWidget = self.create_algorithm_tab_widget()

        # Add widgets to stacked widget and layout
        self.stacked_widget.addWidget(self.algorithm_tab_widget)
        self.stacked_widget.addWidget(self.tsp_instances_widget)
        self.layout.addWidget(self.stacked_widget)

        # Additional buttons below stacked widget
        self.setup_additional_buttons()

    def create_algorithm_tab_widget(self) -> QTabWidget:
        """
        Creates and configures the tab widget for algorithm settings.

        :return: Configured QTabWidget with algorithm setting tabs.
        """
        algorithm_tab_widget = QTabWidget()
        algorithm_tab_widget.setObjectName("algorithmTabWidget")
        algorithm_tab_widget.setStyleSheet("""
            #algorithmTabWidget::pane {  
                background-color: #1E90FF;
                border: 1px solid #424242;
                border-radius: 8px;
            }
            #algorithmTabWidget QTabBar::tab { 
                background-color: #333333;
                color: white;
                padding: 5px 15px;
                margin: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            #algorithmTabWidget QTabBar::tab:selected { 
                background-color: #0074F0;
                color: #fff;
            }
        """)

        # Initialize algorithm setting widgets for each tab
        self.sa_widget: AlgorithmSettingsWidget = AlgorithmSettingsWidget("SA")
        self.sa_ts_widget: AlgorithmSettingsWidget = AlgorithmSettingsWidget("SA + TS")
        self.ts_widget: AlgorithmSettingsWidget = AlgorithmSettingsWidget("TS")

        # Add tabs to the tab widget
        algorithm_tab_widget.addTab(self.sa_widget, "SA")
        algorithm_tab_widget.addTab(self.sa_ts_widget, "SA + TS")
        algorithm_tab_widget.addTab(self.ts_widget, "TS")
        algorithm_tab_widget.setCurrentIndex(1)  # Default tab

        return algorithm_tab_widget

    def setup_signals(self) -> None:
        """
        Connects signals between widgets and the appropriate slot methods for functionality.

        :return: None
        """
        # File selection and algorithm run signals
        self.tsp_instances_widget.file_selected.connect(self.on_file_selected)
        self.sa_widget.run_algorithm_signal.connect(self.emit_run_algorithm_signal)
        self.sa_ts_widget.run_algorithm_signal.connect(self.emit_run_algorithm_signal)
        self.ts_widget.run_algorithm_signal.connect(self.emit_run_algorithm_signal)

        # Button click events
        self.algorithm_settings_button.clicked.connect(self.show_algorithm_parameters_view)
        self.tsp_instances_button.clicked.connect(self.show_load_instances_view)

        # Tab and algorithm finish signals
        self.algorithm_tab_widget.currentChanged.connect(self.tab_changed.emit)
        self.algorithm_tab_widget.currentChanged.connect(self.on_tab_changed)
        self.task_manager.sa_finished_signal.connect(self.on_algorithm_finished)
        self.task_manager.ts_finished_signal.connect(self.on_algorithm_finished)

    # def setup_additional_buttons(self) -> None:
    #     """
    #     Sets up the RUN, STOP, Clear Plots, Generate Report, and Settings buttons in a responsive layout.
    #
    #     RUN and STOP buttons are styled and disabled by default, while the Clear Plots and Generate Report buttons
    #     become enabled after an algorithm finishes running. The Settings button opens a dialog for configuration.
    #     """
    #     additional_buttons_layout: QVBoxLayout = QVBoxLayout()
    #
    #     # Layout for RUN and STOP buttons
    #     run_stop_layout: QHBoxLayout = QHBoxLayout()
    #     self.run_button: QPushButton = QPushButton("RUN")
    #     self.stop_button: QPushButton = QPushButton("STOP")
    #
    #     # RUN button style
    #     run_button_style = """
    #         QPushButton {
    #             font-size: 12px;
    #             color: white;
    #             background-color: #1C3D62; /* Disabled color */
    #             padding: 6px 12px;
    #             border-radius: 4px;
    #         }
    #         QPushButton:enabled {
    #             background-color: #0074F0; /* Enabled color */
    #         }
    #         QPushButton:enabled:hover {
    #             background-color: #0060CD;
    #         }
    #     """
    #     # STOP button style
    #     stop_button_style = """
    #         QPushButton {
    #             font-size: 12px;
    #             color: white;
    #             background-color: #612727; /* Disabled color */
    #             padding: 6px 12px;
    #             border-radius: 4px;
    #         }
    #         QPushButton:enabled {
    #             background-color: #B31B1B; /* Enabled color */
    #         }
    #         QPushButton:enabled:hover {
    #             background-color: #9A1717;
    #         }
    #     """
    #     self.run_button.setStyleSheet(run_button_style)
    #     self.stop_button.setStyleSheet(stop_button_style)
    #     self.run_button.setEnabled(False)
    #     self.stop_button.setEnabled(False)
    #
    #     # Add RUN and STOP buttons to layout
    #     run_stop_layout.addWidget(self.run_button)
    #     run_stop_layout.addWidget(self.stop_button)
    #
    #     # Layout for Clear Plots and Generate Report buttons
    #     clear_report_layout: QHBoxLayout = QHBoxLayout()
    #     self.clear_plots_and_results_button: QPushButton = QPushButton("Clear Plots and Results")
    #     self.clear_plots_and_results_button.setEnabled(False)  # Disabled by default
    #
    #     self.generate_report_button: QPushButton = QPushButton("Generate Report")
    #     self.generate_report_button.setEnabled(False)  # Disabled by default
    #
    #     clear_report_layout.addWidget(self.clear_plots_and_results_button)
    #     clear_report_layout.addWidget(self.generate_report_button)
    #
    #     # Add RUN/STOP and Clear/Report layouts to main layout
    #     additional_buttons_layout.addLayout(run_stop_layout)
    #     additional_buttons_layout.addLayout(clear_report_layout)
    #
    #     # Layout for Settings button at the bottom
    #     settings_layout: QHBoxLayout = QHBoxLayout()
    #     self.settings_button: QPushButton = QPushButton("Settings")
    #     settings_layout.addStretch()  # Center the Settings button
    #     settings_layout.addWidget(self.settings_button)
    #     settings_layout.addStretch()
    #
    #     # Connect button actions to respective methods
    #     self.run_button.clicked.connect(self.on_run_button_clicked)
    #     self.stop_button.clicked.connect(self.on_stop_button_clicked)
    #     self.clear_plots_and_results_button.clicked.connect(self.on_clear_plots_and_results_clicked)
    #     self.generate_report_button.clicked.connect(self.on_generate_report_clicked)  # Generate report action
    #     self.settings_button.clicked.connect(self.open_settings_dialog)
    #
    #     # Add Settings layout and overall button layout to main panel layout
    #     additional_buttons_layout.addLayout(settings_layout)
    #     self.layout.addLayout(additional_buttons_layout)

    def setup_additional_buttons(self) -> None:
        """
        Sets up the RUN, STOP, Clear Plots, Generate Report, and Settings buttons in a responsive layout.

        RUN and STOP buttons are styled and disabled by default, while the Clear Plots and Generate Report buttons
        become enabled after an algorithm finishes running. The Settings button opens a dialog for configuration.
        """
        additional_buttons_layout: QVBoxLayout = QVBoxLayout()
        additional_buttons_layout.setContentsMargins(0, 5, 0, 5)

        # Layout for RUN and STOP buttons
        run_stop_layout: QHBoxLayout = QHBoxLayout()
        self.run_button: QPushButton = QPushButton("RUN")
        self.stop_button: QPushButton = QPushButton("STOP")

        # RUN button style
        run_button_style = """
            QPushButton {
                font-size: 12px;
                color: white;
                background-color: #1C3D62; /* Disabled color */
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:enabled {
                background-color: #0074F0; /* Enabled color */
            }
            QPushButton:enabled:hover {
                background-color: #0060CD;
            }
        """
        # STOP button style
        stop_button_style = """
            QPushButton {
                font-size: 12px;
                color: white;
                background-color: #612727; /* Disabled color */
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:enabled {
                background-color: #B31B1B; /* Enabled color */
            }
            QPushButton:enabled:hover {
                background-color: #9A1717;
            }
        """
        self.run_button.setStyleSheet(run_button_style)
        self.stop_button.setStyleSheet(stop_button_style)
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        # Add RUN and STOP buttons to layout
        run_stop_layout.addWidget(self.run_button)
        run_stop_layout.addWidget(self.stop_button)

        # Layout for Settings, Clear Plots, and Generate Report buttons in one line
        settings_clear_report_layout: QHBoxLayout = QHBoxLayout()
        self.settings_button: QPushButton = QPushButton("Settings")
        self.clear_plots_and_results_button: QPushButton = QPushButton("Clear Plots and Results")
        self.clear_plots_and_results_button.setEnabled(False)  # Disabled by default
        self.generate_report_button: QPushButton = QPushButton("Generate Report")
        self.generate_report_button.setEnabled(False)  # Disabled by default

        # Add all three buttons to the same layout
        settings_clear_report_layout.addWidget(self.settings_button)
        settings_clear_report_layout.addWidget(self.clear_plots_and_results_button)
        settings_clear_report_layout.addWidget(self.generate_report_button)

        # Add RUN/STOP layout and Settings/Clear/Report layout to main layout
        additional_buttons_layout.addLayout(run_stop_layout)
        additional_buttons_layout.addLayout(settings_clear_report_layout)

        # Connect button actions to respective methods
        self.run_button.clicked.connect(self.on_run_button_clicked)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)
        self.clear_plots_and_results_button.clicked.connect(self.on_clear_plots_and_results_clicked)
        self.generate_report_button.clicked.connect(self.on_generate_report_clicked)  # Generate report action
        self.settings_button.clicked.connect(self.open_settings_dialog)

        # Add the overall button layout to the main panel layout
        self.layout.addLayout(additional_buttons_layout)

    def disable_controls_during_run(self) -> None:
        """
        Disables tab switching and 'TSP Instances' button, keeping only the 'STOP' button active.

        :return: None
        """
        self.algorithm_tab_widget.setEnabled(False)
        self.tsp_instances_button.setEnabled(False)
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.clear_plots_and_results_button.setEnabled(False)
        self.generate_report_button.setEnabled(False)

    def enable_controls_after_run(self) -> None:
        """
        Enables tab switching and 'TSP Instances' button after algorithm completion.

        :return: None
        """
        self.algorithm_tab_widget.setEnabled(True)
        self.tsp_instances_button.setEnabled(True)
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.clear_plots_and_results_button.setEnabled(True)
        self.generate_report_button.setEnabled(True)

    def open_settings_dialog(self) -> None:
        """
        Opens the settings dialog for configuring ports and data frequency.

        :return: None
        """
        self.settings_dialog.exec_()

    def show_algorithm_parameters_view(self) -> None:
        """
        Switches view to 'Algorithm Settings' and disables the 'Algorithm Settings' button.

        :return: None
        """
        self.stacked_widget.setCurrentIndex(0)
        self.algorithm_settings_button.setEnabled(False)
        self.tsp_instances_button.setEnabled(True)

    def show_load_instances_view(self) -> None:
        """
        Switches view to 'TSP Instances' and disables the 'TSP Instances' button.

        :return: None
        """
        self.stacked_widget.setCurrentIndex(1)
        self.algorithm_settings_button.setEnabled(True)
        self.tsp_instances_button.setEnabled(False)

    def on_file_selected(self, file_name: str) -> None:
        """
        Handles the file selection signal from TSPInstancesWidget.

        :param file_name: The name of the selected TSP file.
        :return: None
        """
        self.selected_file_name: str = file_name
        self.run_button.setEnabled(True)

    def on_clear_plots_and_results_clicked(self) -> None:
        """
        Clears plots and results, disabling the 'Clear Plots and Results' button.

        :return: None
        """
        self.main_window.visualization_panel.clear_plots_partially()
        self.main_window.results_panel.clear_results_partially()
        self.clear_plots_and_results_button.setEnabled(False)
        self.generate_report_button.setEnabled(False)  # Disable report button after clearing plots

    def on_generate_report_clicked(self) -> None:
        """
        Generates a report and disables the 'Generate Report' button to avoid multiple clicks.

        :return: None
        """
        self.generate_report_button.setEnabled(False)

        # Check if a file name is selected
        if not self.selected_file_name:
            print("No file selected for report generation.")
            return

        # Get instance data for the selected TSP file
        instance_data = self.task_manager.get_instance_data(self.selected_file_name)
        if not instance_data:
            print("Instance data not available.")
            return

        # Determine tab index to gather appropriate algorithm results for the report
        tab_index = self.algorithm_tab_widget.currentIndex()
        algorithm_results, plots = {}, {}

        # Generate report based on selected algorithm(s)
        if tab_index == 0:  # SA
            algorithm_results["SA"] = {
                "parameters": self.sa_widget.sa_settings_widget.collect_sa_parameters().to_dict(),
                "best_cost": int(self.main_window.results_panel.value_best_cost_sa.text()),
                "relative_error": self.main_window.results_panel.value_relative_error_best_sa.text(),
            }
            plots["SA"] = {
                "cost_plot": self.main_window.visualization_panel.cost_plot_widget_sa.get_plot_data(),
            }
        elif tab_index == 1:  # SA + TS
            algorithm_results["SA"] = {
                "parameters": self.sa_ts_widget.sa_settings_widget.collect_sa_parameters().to_dict(),
                "best_cost": int(self.main_window.results_panel.value_best_cost_sa.text()),
                "relative_error": self.main_window.results_panel.value_relative_error_best_sa.text(),
            }
            plots["SA"] = {
                "cost_plot": self.main_window.visualization_panel.cost_plot_widget_sa.get_plot_data(),
            }

            algorithm_results["TS"] = {
                "parameters": self.sa_ts_widget.ts_settings_widget.collect_ts_parameters().to_dict(),
                "best_cost": int(self.main_window.results_panel.value_best_cost_ts.text()),
                "relative_error": self.main_window.results_panel.value_relative_error_best_ts.text(),
            }
            plots["TS"] = {
                "cost_plot": self.main_window.visualization_panel.cost_plot_widget_ts.get_plot_data(),
            }
        elif tab_index == 2:  # TS
            algorithm_results["TS"] = {
                "parameters": self.ts_widget.ts_settings_widget.collect_ts_parameters().to_dict(),
                "best_cost": int(self.main_window.results_panel.value_best_cost_ts.text()),
                "relative_error": self.main_window.results_panel.value_relative_error_best_ts.text(),
            }
            plots["TS"] = {
                "cost_plot": self.main_window.visualization_panel.cost_plot_widget_ts.get_plot_data(),
            }

        # Send data to TaskManager for report generation
        self.task_manager.generate_report(self.selected_file_name, instance_data, algorithm_results, plots)

    def on_run_button_clicked(self) -> None:
        """
        Handles the RUN button click and emits a signal to start the algorithm.

        :return: None
        """
        current_tab = self.algorithm_tab_widget.currentWidget()
        if isinstance(current_tab, AlgorithmSettingsWidget):
            algorithms = []
            if current_tab.algorithm_type == "SA":
                algorithms.append("SA")
            elif current_tab.algorithm_type == "TS":
                algorithms.append("TS")
            elif current_tab.algorithm_type == "SA + TS":
                algorithms.extend(["SA", "TS"])

            # Emit signal with selected algorithms and their parameters
            self.emit_run_algorithm_signal(algorithms)

            # Disable controls while algorithm is running
            self.disable_controls_during_run()

    def on_stop_button_clicked(self) -> None:
        """
        Handles the STOP button click to halt the algorithm.

        :return: None
        """
        self.task_manager.stop_algorithms()  # Call TaskManager to stop algorithms
        self.enable_controls_after_run()

    def on_tab_changed(self) -> None:
        """
        Clears plots and results upon switching between tabs, disabling relevant buttons.

        :return: None
        """
        self.main_window.visualization_panel.clear_plots_partially()
        self.main_window.results_panel.clear_results_partially()
        self.clear_plots_and_results_button.setEnabled(False)
        self.generate_report_button.setEnabled(False)

    def emit_run_algorithm_signal(self, algorithms: list[str]) -> None:
        """
        Emits the run_algorithm_signal with the selected algorithms and their parameters.

        :param algorithms: The list of selected algorithms.
        :return: None
        """
        if self.selected_file_name:
            sa_params, ts_params = None, None

            # Collect parameters based on selected algorithms
            if "SA" in algorithms and "TS" in algorithms:
                if hasattr(self.sa_ts_widget, 'sa_settings_widget') and hasattr(self.sa_ts_widget, 'ts_settings_widget'):
                    sa_params = self.sa_ts_widget.sa_settings_widget.collect_sa_parameters()
                    ts_params = self.sa_ts_widget.ts_settings_widget.collect_ts_parameters()
            else:
                if "SA" in algorithms and hasattr(self.sa_widget, 'sa_settings_widget'):
                    sa_params = self.sa_widget.sa_settings_widget.collect_sa_parameters()
                if "TS" in algorithms and hasattr(self.ts_widget, 'ts_settings_widget'):
                    ts_params = self.ts_widget.ts_settings_widget.collect_ts_parameters()

            sa_port = int(self.settings_dialog.sa_port_input.text())
            ts_port = int(self.settings_dialog.ts_port_input.text())
            data_frequency = int(self.settings_dialog.data_frequency_input.text())

            # Create AlgorithmConfig object with selected parameters
            config = AlgorithmConfig(
                algorithms=algorithms,
                file_name=self.selected_file_name,
                sa_params=sa_params,
                sa_port=sa_port,
                ts_params=ts_params,
                ts_port=ts_port,
                data_frequency=data_frequency
            )

            # Emit signal to start the algorithm with the selected configuration
            self.run_algorithm_signal.emit(config)

    def on_algorithm_finished(self) -> None:
        """
        Handles algorithm completion by enabling controls only after both SA and TS algorithms have finished.

        :return: None
        """
        current_tab = self.algorithm_tab_widget.currentWidget()
        # Check if the current tab is an AlgorithmSettingsWidget
        if isinstance(current_tab, AlgorithmSettingsWidget):
            # Check if the current configuration includes both algorithms (SA + TS)
            if current_tab.algorithm_type == "SA + TS":
                # Ensure both algorithms have completed
                if not self.task_manager.algorithms_manager_dict["SA"].is_receiving and not \
                        self.task_manager.algorithms_manager_dict["TS"].is_receiving:
                    self.enable_controls_after_run()
                    self.clear_plots_and_results_button.setEnabled(True)
                    self.generate_report_button.setEnabled(True)
            # Otherwise, check if the current algorithm has finished
            else:
                self.enable_controls_after_run()
                self.clear_plots_and_results_button.setEnabled(True)
                self.generate_report_button.setEnabled(True)
