# src/gui/components/plots/city_map_widget.py

import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
import numpy as np


class CityMapWidget(QWidget):
    def __init__(self, parent=None, coordinates=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Inicjalizacja widgetu wykresu
        self.plot = pg.PlotWidget()
        self.layout.addWidget(self.plot)

        # Inicjalizacja danych
        self.coordinates = coordinates or []  # Lista z koordynatami miast (x, y)
        self.data_x = []  # Lista dla osi X (koordynaty x miast)
        self.data_y = []  # Lista dla osi Y (koordynaty y miast)
        self.route = []  # Lista, która będzie aktualizowana z aktualną trasą

        # Utwórz scatter plot dla miast
        self.scatter = pg.ScatterPlotItem(pen=pg.mkPen(None), symbol='o', brush='g')
        self.plot.addItem(self.scatter)

        # Utwórz linię, która będzie reprezentować trasę
        self.route_line = pg.PlotCurveItem(pen='b')
        self.plot.addItem(self.route_line)

        # Zaktualizuj pozycje miast
        self.set_city_positions()

    def set_city_positions(self):
        """
        Ustawienia pozycji miast na mapie na podstawie współrzędnych.
        """
        if self.coordinates:
            # Ustawienia dla data_x i data_y
            self.data_x, self.data_y = zip(*self.coordinates)
            self.scatter.setData(self.data_x, self.data_y)

    def update_route(self, current_solution: list[int]):
        """
        Aktualizuje wykres mapy miast na podstawie bieżącego rozwiązania (trasy).
        """
        try:
            # Utwórz trasę na podstawie bieżącego rozwiązania (permutacji miast)
            self.route = [(self.data_x[i], self.data_y[i]) for i in current_solution]

            # Dodaj pierwszy punkt na końcu, aby zamknąć trasę
            self.route.append((self.data_x[current_solution[0]], self.data_y[current_solution[0]]))

            route_x, route_y = zip(*self.route)

            # Konwertuj route_x i route_y na numpy array, aby były 1D ndarray
            route_x = np.array(route_x)
            route_y = np.array(route_y)

            # Aktualizujemy linię trasy
            self.route_line.setData(route_x, route_y)

        except IndexError as e:
            print(f"IndexError encountered while updating route: {e}")
            return

    def clear_route(self):
        """
        Czyści wykres miasta i tras.
        """
        self.route_line.setData([], [])  # Wyczyść linię trasy
        self.route.clear()  # Wyczyść trasę

    def clear_all(self):
        """
        Czyści wszystkie dane na wykresie.
        """
        self.clear_route() # Wyczyść trasę
        self.scatter.setData([], []) # Wyczyść scatter plot miast
        self.data_x = [] # Resetuj dane osi X
        self.data_y = [] # Resetuj dane osi Y