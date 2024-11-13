# src/gui/widgets/cost_plot_widget.py

import pyqtgraph as pg
from typing import Optional
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout


class CostPlotWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, title: str = "Cost Over Time",
                 x_axis_label: str = "Time [ms]", y_axis_label: str = "Cost") -> None:
        """
        Initializes the CostPlotWidget, setting up a line plot to display the cost over time.

        :param parent: Optional parent widget.
        :param title: Title displayed at the top of the plot.
        :param x_axis_label: Label for the x-axis, typically representing time in milliseconds.
        :param y_axis_label: Label for the y-axis, typically representing the cost.
        :return: None
        """
        super().__init__(parent)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Plot setup with title and axis labels
        self.plot: pg.PlotWidget = pg.PlotWidget()
        self.plot.setTitle(title, color='w', size="16pt")
        self.plot.setLabel('left', y_axis_label)
        self.plot.setLabel('bottom', x_axis_label)
        self.plot.setBackground('#464646')

        # Style settings for axes
        self.set_axis_styles('bottom')
        self.set_axis_styles('left')

        self.layout.addWidget(self.plot)

        # Data initialization
        self.data_x: list[int] = []  # X-axis data representing time in ms
        self.data_y: list[int] = []  # Y-axis data representing cost

        # Line plot item for displaying the cost curve
        self.curve: pg.PlotDataItem = self.plot.plot(self.data_x, self.data_y, pen='#FF8315')

    def set_axis_styles(self, axis_name: str) -> None:
        """
        Configures the visual style for a given axis.

        :param axis_name: The name of the axis, either 'bottom' or 'left'.
        :return: None
        """
        axis_font: QFont = QFont()
        axis_font.setPointSize(12)

        axis_item: pg.AxisItem = self.plot.getAxis(axis_name)
        axis_item.setStyle(tickFont=axis_font, tickLength=-10)
        axis_item.label.setFont(axis_font)
        axis_item.setTextPen('w')
        axis_item.setTickPen('w')
        axis_item.setPen('w')

    def update_plot(self, current_time: int, current_cost: int) -> None:
        """
        Updates the plot with new data for time and cost.

        :param current_time: The current elapsed time in milliseconds.
        :param current_cost: The current cost associated with the solution at this time.
        :return: None
        """
        self.data_x.append(current_time)
        self.data_y.append(current_cost)

        # Update curve with the new data
        self.curve.setData(self.data_x, self.data_y)

    def clear(self) -> None:
        """
        Clears all data from the plot, resetting it to an empty state.

        :return: None
        """
        self.data_x.clear()
        self.data_y.clear()
        self.curve.setData(self.data_x, self.data_y)

    def get_plot_data(self) -> dict[str, list[int]]:
        """
        Returns the plot data in dictionary format for further processing or saving.

        :return: Dictionary containing x-axis (time) and y-axis (cost) data.
        """
        return {'x': self.data_x, 'y': self.data_y}
