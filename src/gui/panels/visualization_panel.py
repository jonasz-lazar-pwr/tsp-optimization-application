# src/gui/panels/visualization_panel.py

from typing import Optional
from PySide6.QtWidgets import QWidget, QGridLayout, QSpacerItem, QSizePolicy

from src.gui.widgets.visualization.cost_plot_widget import CostPlotWidget
from src.gui.widgets.visualization.city_plot_widget import CityPlotWidget


class VisualizationPanel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the VisualizationPanel, setting up widgets and layout for displaying plots for Simulated Annealing
        and Tabu Search.

        :param parent: Optional parent widget.
        :return: None
        """
        super().__init__(parent)

        # Initialize layout and plot widgets
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Initialize plots and layout structure
        self.setup_plot_widgets()
        self.setup_spacers()
        self.initialize_layout()

    def setup_plot_widgets(self) -> None:
        """
        Initializes the plot widgets for displaying cost and route for both Simulated Annealing and Tabu Search.

        :return: None
        """
        self.cost_plot_widget_sa: CostPlotWidget = CostPlotWidget(self, "Simulated Annealing - Cost Over Time")
        self.city_plot_widget_sa: CityPlotWidget = CityPlotWidget(self, "Simulated Annealing - Current Route")
        self.cost_plot_widget_ts: CostPlotWidget = CostPlotWidget(self, "Tabu Search - Cost Over Time")
        self.city_plot_widget_ts: CityPlotWidget = CityPlotWidget(self, "Tabu Search - Current Route")

    def setup_spacers(self) -> None:
        """
        Initializes spacer items for dynamic adjustments in the layout.

        :return: None
        """
        self.vertical_spacer_top: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_spacer_bottom: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontal_spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

    def initialize_layout(self) -> None:
        """
        Sets the initial layout structure for the VisualizationPanel by adding plot widgets in a 2x2 grid.

        :return: None
        """
        self.layout.addWidget(self.cost_plot_widget_sa, 0, 0)
        self.layout.addWidget(self.city_plot_widget_sa, 0, 1)
        self.layout.addWidget(self.cost_plot_widget_ts, 1, 0)
        self.layout.addWidget(self.city_plot_widget_ts, 1, 1)

        # Apply the main layout to the widget
        self.setLayout(self.layout)

    def adjust_layout(self, tab_index: int, coordinates_available: bool) -> None:
        """
        Adjusts the layout based on the selected algorithm tab and the availability of coordinates.

        :param tab_index: The selected tab index (0 for SA, 1 for SA + TS, 2 for TS).
        :param coordinates_available: Flag indicating if coordinates are available for route plotting.
        :return: None
        """
        # Reset layout and visibility
        self.reset_layout()

        # Adjust layout based on the selected tab and coordinates
        if tab_index == 0:
            self.configure_sa_layout(coordinates_available)
        elif tab_index == 1:
            self.configure_sa_ts_layout(coordinates_available)
        elif tab_index == 2:
            self.configure_ts_layout(coordinates_available)

    def reset_layout(self) -> None:
        """
        Resets the layout by removing spacer items and hiding all plot widgets.

        :return: None
        """
        self.layout.removeItem(self.vertical_spacer_top)
        self.layout.removeItem(self.vertical_spacer_bottom)
        self.layout.removeItem(self.horizontal_spacer)
        self.set_all_plots_visible(False)

    def configure_sa_layout(self, coordinates_available: bool) -> None:
        """
        Configures the layout for the Simulated Annealing (SA) algorithm.

        :param coordinates_available: Flag indicating if coordinates are available for route plotting.
        :return: None
        """
        self.cost_plot_widget_sa.setVisible(True)
        if coordinates_available:
            self.city_plot_widget_sa.setVisible(True)
            # Center vertically with top and bottom spacers
            self.layout.addItem(self.vertical_spacer_top, 0, 0, 1, 2)
            self.layout.addWidget(self.cost_plot_widget_sa, 1, 0)
            self.layout.addWidget(self.city_plot_widget_sa, 1, 1)
            self.layout.addItem(self.vertical_spacer_bottom, 2, 0, 1, 2)
        else:
            # Center horizontally and vertically with surrounding spacers
            self.layout.addItem(self.vertical_spacer_top, 0, 1)
            self.layout.addWidget(self.cost_plot_widget_sa, 1, 1)
            self.layout.addItem(self.vertical_spacer_bottom, 2, 1)
            self.layout.addItem(self.horizontal_spacer, 1, 0)
            self.layout.addItem(self.horizontal_spacer, 1, 2)

    def configure_sa_ts_layout(self, coordinates_available: bool) -> None:
        """
        Configures the layout for Simulated Annealing and Tabu Search (SA + TS) algorithms.

        :param coordinates_available: Flag indicating if coordinates are available for route plotting.
        :return: None
        """
        self.cost_plot_widget_sa.setVisible(True)
        self.cost_plot_widget_ts.setVisible(True)
        if coordinates_available:
            self.city_plot_widget_sa.setVisible(True)
            self.city_plot_widget_ts.setVisible(True)
            # Default 2x2 grid configuration
            self.layout.addWidget(self.cost_plot_widget_sa, 0, 0)
            self.layout.addWidget(self.city_plot_widget_sa, 0, 1)
            self.layout.addWidget(self.cost_plot_widget_ts, 1, 0)
            self.layout.addWidget(self.city_plot_widget_ts, 1, 1)
        else:
            # Center horizontally, with plots stacked vertically
            self.layout.addItem(self.vertical_spacer_top, 0, 1)
            self.layout.addWidget(self.cost_plot_widget_sa, 1, 1)
            self.layout.addWidget(self.cost_plot_widget_ts, 2, 1)
            self.layout.addItem(self.vertical_spacer_bottom, 3, 1)
            self.layout.addItem(self.horizontal_spacer, 1, 0)
            self.layout.addItem(self.horizontal_spacer, 1, 2)

    def configure_ts_layout(self, coordinates_available: bool) -> None:
        """
        Configures the layout for the Tabu Search (TS) algorithm.

        :param coordinates_available: Flag indicating if coordinates are available for route plotting.
        :return: None
        """
        self.cost_plot_widget_ts.setVisible(True)
        if coordinates_available:
            self.city_plot_widget_ts.setVisible(True)
            # Center vertically, with both plots in a single row
            self.layout.addItem(self.vertical_spacer_top, 0, 0, 1, 2)
            self.layout.addWidget(self.cost_plot_widget_ts, 1, 0)
            self.layout.addWidget(self.city_plot_widget_ts, 1, 1)
            self.layout.addItem(self.vertical_spacer_bottom, 2, 0, 1, 2)
        else:
            # Center horizontally and vertically for Cost Plot only
            self.layout.addItem(self.vertical_spacer_top, 0, 1)
            self.layout.addWidget(self.cost_plot_widget_ts, 1, 1)
            self.layout.addItem(self.vertical_spacer_bottom, 2, 1)
            self.layout.addItem(self.horizontal_spacer, 1, 0)
            self.layout.addItem(self.horizontal_spacer, 1, 2)

    def update_sa_plots(self, elapsed_time: int, current_cost: int, current_solution: list[int]) -> None:
        """
        Updates the Simulated Annealing (SA) data visualization.

        This method updates the cost over time plot and current route visualization for the SA algorithm.
        It only updates each plot if it is currently visible.

        :param elapsed_time: The elapsed time in milliseconds since the algorithm started.
        :param current_cost: The current cost of the solution at this time.
        :param current_solution: The current route solution represented as a list of city indices.
        :return: None
        """
        if self.cost_plot_widget_sa.isVisible():
            self.cost_plot_widget_sa.update_plot(elapsed_time, current_cost)
        if self.city_plot_widget_sa.isVisible():
            self.city_plot_widget_sa.update_route(current_solution)

    def update_ts_plots(self, elapsed_time: int, current_cost: int, current_solution: list[int]) -> None:
        """
        Updates the Tabu Search (TS) data visualization.

        This method updates the cost over time plot and current route visualization for the TS algorithm.
        It only updates each plot if it is currently visible.

        :param elapsed_time: The elapsed time in milliseconds since the algorithm started.
        :param current_cost: The current cost of the solution at this time.
        :param current_solution: The current route solution represented as a list of city indices.
        :return: None
        """
        if self.cost_plot_widget_ts.isVisible():
            self.cost_plot_widget_ts.update_plot(elapsed_time, current_cost)
        if self.city_plot_widget_ts.isVisible():
            self.city_plot_widget_ts.update_route(current_solution)

    def set_all_plots_visible(self, visible: bool) -> None:
        """
        Shows or hides all plots based on the `visible` parameter.

        This method adjusts the visibility of each plot widget within the visualization panel.

        :param visible: A boolean value indicating whether to show (True) or hide (False) all plots.
        :return: None
        """
        self.cost_plot_widget_sa.setVisible(visible)
        self.city_plot_widget_sa.setVisible(visible)
        self.cost_plot_widget_ts.setVisible(visible)
        self.city_plot_widget_ts.setVisible(visible)

    def update_city_map_data(self, coordinates: list[tuple[float, float]]) -> None:
        """
        Updates city coordinates for the city map plots without displaying them.

        This method sets new coordinates for each city plot widget but does not make the plots visible.

        :param coordinates: A list of tuples, where each tuple represents the (x, y) coordinates of a city.
        :return: None
        """
        self.city_plot_widget_sa.coordinates = coordinates
        self.city_plot_widget_sa.set_city_positions()
        self.city_plot_widget_ts.coordinates = coordinates
        self.city_plot_widget_ts.set_city_positions()

    def clear_plots_partially(self) -> None:
        """
        Clears the data from the cost and route plots while retaining city positions.

        This method removes the current cost data and routes from both the SA and TS plots,
        but keeps the static city positions on the city maps intact.

        :return: None
        """
        self.cost_plot_widget_sa.clear()
        self.cost_plot_widget_ts.clear()
        self.city_plot_widget_sa.clear_route()
        self.city_plot_widget_ts.clear_route()

    def clear_plots(self) -> None:
        """
        Fully clears all data from the plots, including city positions and routes.

        This method completely resets each plot by removing both the routes and city positions,
        ensuring a blank slate for all visualizations.

        :return: None
        """
        self.clear_plots_partially()
        self.city_plot_widget_sa.clear_cities()
        self.city_plot_widget_ts.clear_cities()