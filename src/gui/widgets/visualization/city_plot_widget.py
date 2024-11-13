# src/gui/widgets/city_plot_widget.py

import pyqtgraph as pg
import numpy as np
from typing import Optional
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout


class CityPlotWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, title: str = "Current Route",
                 x_axis_label: str = "X-coordinates", y_axis_label: str = "Y-coordinates",
                 coordinates: Optional[list[tuple[float, float]]] = None) -> None:
        """
        Initializes the CityPlotWidget, setting up the layout, plot, and visual elements
        for displaying city positions and a route on a 2D map.

        :param parent: Optional parent widget.
        :param title: Title of the plot.
        :param x_axis_label: Label for the x-axis.
        :param y_axis_label: Label for the y-axis.
        :param coordinates: Optional list of tuples with city coordinates [(x1, y1), (x2, y2), ...].
        """
        super().__init__(parent)

        # Layout for organizing plot components
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Initialize the plot with title and axis labels
        self.plot: pg.PlotWidget = pg.PlotWidget()
        self.plot.setTitle(title, color='w', size="16pt")  # Set a larger title font
        self.plot.setLabel('left', y_axis_label)
        self.plot.setLabel('bottom', x_axis_label)
        self.plot.setBackground('#464646')  # Dark background for contrast

        # Style the axes for improved readability
        self.set_axis_styles('bottom')
        self.set_axis_styles('left')

        # Add the plot to the main layout
        self.layout.addWidget(self.plot)

        # Data initialization
        self.coordinates: list[tuple[float, float]] = coordinates or []  # City coordinates [(x, y)]
        self.data_x: list[float] = []  # X-coordinates of cities
        self.data_y: list[float] = []  # Y-coordinates of cities
        self.route: list[tuple[float, float]] = []  # Current route path

        # Create scatter plot item for city positions
        self.scatter: pg.ScatterPlotItem = pg.ScatterPlotItem(pen=pg.mkPen(None), symbol='o', brush='w')
        self.plot.addItem(self.scatter)

        # Create line item for visualizing the route between cities
        self.route_line: pg.PlotCurveItem = pg.PlotCurveItem(pen='g')
        self.plot.addItem(self.route_line)

        # Set initial positions of cities on the plot
        self.set_city_positions()

    def set_axis_styles(self, axis_name: str) -> None:
        """
        Configures the style for a specified axis, including font size, tick length,
        and color settings for improved readability on a dark background.

        :param axis_name: The name of the axis to style ('bottom' for x-axis or 'left' for y-axis).
        :return: None
        """
        # Define font properties for the axis
        axis_font: QFont = QFont()
        axis_font.setPointSize(12)

        # Access the specified axis from the plot
        axis_item = self.plot.getAxis(axis_name)
        # Apply style settings to the axis
        axis_item.setStyle(tickFont=axis_font, tickLength=-10)
        axis_item.label.setFont(axis_font)
        axis_item.setTextPen('w')  # Set the color for axis text to white
        axis_item.setTickPen('w')  # Set the color for axis ticks to white
        axis_item.setPen('w')  # Set the color for the axis line to white

    def set_city_positions(self) -> None:
        """
        Sets the positions of cities on the map based on the provided coordinates.
        Updates the scatter plot data to display each city as a point on the plot.

        :return: None
        """
        if self.coordinates:
            # Extract x and y coordinates from the list of (x, y) tuples
            self.data_x, self.data_y = zip(*self.coordinates)
            # Update the scatter plot with the city positions
            self.scatter.setData(self.data_x, self.data_y)

    def update_route(self, current_solution: list[int]) -> None:
        """
        Updates the city map to display the current route based on the solution provided.
        The route connects cities in the order specified in `current_solution`.

        :param current_solution: List of city indices representing the current route as a permutation of city indices.
        :return: None
        """
        try:
            # Create the route based on the current solution (permutation of city indices)
            self.route = [(self.data_x[i], self.data_y[i]) for i in current_solution]

            # Add the starting city at the end to close the route
            self.route.append((self.data_x[current_solution[0]], self.data_y[current_solution[0]]))

            # Extract x and y coordinates for the route
            route_x, route_y = zip(*self.route)

            # Convert route_x and route_y to numpy arrays for compatibility with pyqtgraph
            route_x = np.array(route_x)
            route_y = np.array(route_y)

            # Update the route line on the plot
            self.route_line.setData(route_x, route_y)

        except IndexError as e:
            print(f"IndexError encountered while updating route: {e}")
            return

    def clear_route(self) -> None:
        """
        Clears the visual representation of the current route from the map.
        This method only affects the route line, leaving city markers intact.

        :return: None
        """
        self.route.clear()  # Clear the stored route data
        self.route_line.setData([], [])  # Clear the route line on the plot

    def clear_cities(self) -> None:
        """
        Clears the visual representation of city markers from the map.
        This method only affects the city markers and resets the coordinates list.

        :return: None
        """
        self.scatter.setData([], [])  # Clear the scatter plot for city markers
        self.coordinates = []  # Reset the coordinates list
