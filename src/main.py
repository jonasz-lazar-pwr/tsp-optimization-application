# src/main.py

import sys
from PySide6.QtWidgets import QApplication
from src.utils.path_config import PROJECT_ROOT

# Append the project directory to the Python path
sys.path.append(PROJECT_ROOT)

from src.backend.task_manager import TaskManager
from src.gui.main_window import MainWindow


def main():
    """
    Main function to initialize and launch the TSP Optimization application.

    - Initializes QApplication to manage the GUI application.
    - Creates TaskManager to manage backend tasks and algorithms.
    - Initializes MainWindow with the TaskManager instance, connecting the GUI with backend processes.
    - Shows the main window and starts the application's event loop.

    :return: None
    """
    # Initialize QApplication
    app: QApplication = QApplication(sys.argv)

    # Initialize TaskManager for managing algorithms and tasks
    task_manager: TaskManager = TaskManager()

    # Initialize MainWindow with the TaskManager instance
    main_window: MainWindow = MainWindow(task_manager)

    # Show the main window GUI
    main_window.show()

    # Start the main event loop of the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
