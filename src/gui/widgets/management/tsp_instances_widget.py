# src/gui/widgets/management/tsp_instances_widget.py

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView


class TSPInstancesWidget(QWidget):
    file_selected = Signal(str)  # Sygnał informujący o wyborze pliku

    def __init__(self, task_manager, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.layout = QVBoxLayout(self)

        # Przycisk do ładowania plików
        self.load_files_button = QPushButton("Load Files")
        self.load_files_button.clicked.connect(self.load_instance_files)

        # Konfiguracja tabeli
        self.instance_table = QTableWidget(0, 3)
        self.instance_table.setHorizontalHeaderLabels(["Name", "Dimension", "Coordinates"])
        header = self.instance_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.instance_table.verticalHeader().setVisible(False)
        self.instance_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.instance_table.setShowGrid(False)
        self.instance_table.setStyleSheet("""
            QTableWidget::item { 
                border-bottom: 1px solid #424242;
                text-align: center;
            }
            QHeaderView::section {
                background-color: #4C4C4C;
                border: 1px solid #424242; 
                height: 30px;
                text-align: center;
            }
        """)
        self.instance_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.instance_table.cellClicked.connect(self.select_instance)

        # Dodanie elementów do layoutu
        self.layout.addWidget(self.load_files_button)
        self.layout.addWidget(self.instance_table)

        self.setLayout(self.layout)

    def load_instance_files(self):
        """
        Ładuje pliki TSP i aktualizuje tabelę.
        """
        self.task_manager.select_tsp_directory()
        self.update_file_list()

    def update_file_list(self):
        """
        Aktualizuje listę plików w tabeli.
        """
        self.instance_table.setRowCount(0)
        files_data = self.task_manager.get_files_data_for_table()

        for name, dimension, has_coordinates in files_data:
            row_position = self.instance_table.rowCount()
            self.instance_table.insertRow(row_position)

            name_item = QTableWidgetItem(name)
            dimension_item = QTableWidgetItem(dimension)
            coordinates_item = QTableWidgetItem(has_coordinates)

            name_item.setTextAlignment(Qt.AlignCenter)
            dimension_item.setTextAlignment(Qt.AlignCenter)
            coordinates_item.setTextAlignment(Qt.AlignCenter)

            self.instance_table.setItem(row_position, 0, name_item)
            self.instance_table.setItem(row_position, 1, dimension_item)
            self.instance_table.setItem(row_position, 2, coordinates_item)

    def select_instance(self, row: int, column: int):
        """
        Obsługuje wybór instancji z tabeli.

        :param row: Wybrany wiersz w tabeli.
        :param column: Kolumna, w którą kliknięto (nie jest używana w tej funkcji).
        """
        # Pobierz nazwę instancji z pierwszej kolumny wybranego wiersza
        selected_instance_name = self.instance_table.item(row, 0).text()
        self.file_selected.emit(selected_instance_name)
