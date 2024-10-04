# src/gui/main_window.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QComboBox
from src.backend.task_manager import TaskManager


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
        self.task_manager.solution_signal.connect(self.update_current_solution)
        self.task_manager.result_signal.connect(self.update_result)

        # Layout setup
        layout = QVBoxLayout()

        # Dodaj QComboBox do wyboru pliku TSP
        self.file_selector = QComboBox()
        self.file_selector.currentIndexChanged.connect(self.on_file_selection_change)
        layout.addWidget(self.file_selector)

        # Button to run the Simulated Annealing algorithm
        self.run_button = QPushButton("Run Simulated Annealing")
        self.run_button.clicked.connect(self.run_simulated_annealing)
        layout.addWidget(self.run_button)

        # Button to select a directory with TSP files
        self.select_directory_button = QPushButton("Select TSP Directory")
        self.select_directory_button.clicked.connect(self.select_directory)
        layout.addWidget(self.select_directory_button)

        # Labels for displaying results
        self.result_label = QLabel("Final result will be shown here")
        layout.addWidget(self.result_label)

        self.current_solution_label = QLabel("Current solution will be shown here")
        layout.addWidget(self.current_solution_label)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_directory(self) -> None:
        """
        Method for handling directory selection for TSP files.
        """
        self.task_manager.select_tsp_directory()
        self.update_file_selector()

    def update_file_selector(self) -> None:
        file_names = self.task_manager.get_loaded_file_names()
        self.file_selector.clear()
        self.file_selector.addItems(file_names)

    def on_file_selection_change(self) -> None:
        selected_file = self.file_selector.currentText()
        print(f"Selected file: {selected_file}")  # Debug print

    def run_simulated_annealing(self) -> None:
        """
        Method for handling the execution of the Simulated Annealing algorithm.
        """
        selected_file = self.file_selector.currentText()
        if selected_file:
            temperature = 10000.0
            iterations = 100000
            self.task_manager.start_simulated_annealing_for_file(selected_file, temperature, iterations)
        else:
            print("No file selected.")  # Debug print

    def update_current_solution(self, solution: list[float]) -> None:
        """
        Updates the label displaying the current solution.

        :param solution: A list representing the current solution.
        """
        self.current_solution_label.setText(f"Current solution: {solution}")

    def update_result(self, result: float) -> None:
        """
        Updates the label displaying the final result.

        :param result: The cost of the final solution.
        """
        self.result_label.setText(f"Final cost: {result}")
