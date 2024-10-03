# src/main.py

import sys
from PySide6.QtWidgets import QApplication
from src.backend.task_manager import TaskManager
from src.gui.main_window import MainWindow
from src.config import PROJECT_ROOT

# Append the project directory to the Python path
sys.path.append(str(PROJECT_ROOT))


def main():
    # Inicjalizacja QApplication
    app = QApplication(sys.argv)

    # Inicjalizacja Backend
    backend = TaskManager()

    # Inicjalizacja GUI i wstrzyknięcie backendu
    gui = MainWindow(backend)

    # Uruchomienie GUI
    gui.show()

    # Uruchomienie głównej pętli zdarzeń aplikacji
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
