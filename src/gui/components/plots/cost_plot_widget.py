# src/gui/components/plots/cost_plot_widget.py

import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout


class CostPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Utwórz wykres
        self.plot = pg.PlotWidget()
        self.layout.addWidget(self.plot)

        # Inicjalizacja danych
        self.data_x = []  # Oś X (czas)
        self.data_y = []  # Oś Y (koszt)

        # Dodaj wykres liniowy
        self.curve = self.plot.plot(self.data_x, self.data_y, pen='r')

    def update_plot(self, current_time: int, current_cost: int):
        """
        Aktualizuje wykres na podstawie nowych danych.
        """
        self.data_x.append(current_time)
        self.data_y.append(current_cost)

        # Zaktualizuj dane na wykresie
        self.curve.setData(self.data_x, self.data_y)

    def clear(self):
        """
        Czyści wykres.
        """
        self.data_x.clear()
        self.data_y.clear()
        self.curve.setData(self.data_x, self.data_y)