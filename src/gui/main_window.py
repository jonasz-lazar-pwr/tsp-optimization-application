# src/gui/main_window.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from src.backend.task_manager import TaskManager


class MainWindow(QMainWindow):
    def __init__(self, task_manager: TaskManager) -> None:
        """
        Initializes the main application window.

        :param task_manager: An instance of TaskManager responsible for managing tasks.
        """
        super().__init__()
        self.setWindowTitle("TSP Optimization Application")

        # Inject the TaskManager instance
        self.task_manager = task_manager

        # Layout setup
        layout = QVBoxLayout()

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

    def run_simulated_annealing(self) -> None:
        """
        Method for handling the execution of the Simulated Annealing algorithm.
        """
        temperature: float = 10000.0
        iterations: int = 100000
        distance_matrix: list[list[float]] = [
            # ... (distance matrix here)
        ]

        # Start the algorithm in the background
        self.task_manager.start_simulated_annealing(distance_matrix, temperature, iterations)

    def select_directory(self) -> None:
        """
        Method for handling directory selection for TSP files.
        """
        self.task_manager.select_tsp_directory()

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
