# src/main.py

import sys
from PySide6.QtWidgets import QApplication
from src.utils.path_config import PROJECT_ROOT

# Append the project directory to the Python path
sys.path.append(PROJECT_ROOT)

from src.backend.task_manager import TaskManager
from src.gui.main_window import MainWindow


def main():
    # Inicjalizacja QApplication
    app = QApplication(sys.argv)

    # Inicjalizacja TaskManager
    task_manager = TaskManager()

    # Inicjalizacja GUI z podłączonym TaskManagerem
    main_window = MainWindow(task_manager)

    # Uruchomienie GUI
    main_window.show()

    # Uruchomienie głównej pętli zdarzeń aplikacji
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
