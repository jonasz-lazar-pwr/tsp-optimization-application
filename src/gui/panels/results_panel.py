# src/gui/panels/results_panel.py

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QLineEdit, QLabel, QSpacerItem, QSizePolicy


class ResultsPanel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the ResultsPanel, setting up the layout and widgets for displaying algorithm results.

        :param parent: Optional parent widget.
        :return: None
        """
        super().__init__(parent)

        # Main layout for ResultsPanel
        self.layout: QGridLayout = QGridLayout(self)
        self.fixed_width: int = 350  # Fixed width for result boxes

        # Group box for Simulated Annealing (SA) results
        self.sa_group_box: QGroupBox = QGroupBox("Simulated Annealing Results")
        self.sa_group_box.setStyleSheet("""
            QGroupBox {
                font-size: 13pt;
            }
        """)
        self.sa_group_box.setFixedWidth(self.fixed_width)
        sa_layout: QGridLayout = QGridLayout()

        # Row 1: Optimal Cost for SA
        sa_layout.addWidget(self.create_label("Optimal Cost:"), 0, 0)
        self.value_optimal_cost_sa: QLineEdit = self.create_line_edit("0", width=80)
        sa_layout.addWidget(self.value_optimal_cost_sa, 0, 1)

        # Row 2: Current Cost and Error for SA
        sa_layout.addWidget(self.create_label("Current Cost / Error:"), 1, 0)
        self.value_current_cost_sa: QLineEdit = self.create_line_edit("0", width=80)
        self.value_relative_error_current_sa: QLineEdit = self.create_line_edit("0%", width=80)
        sa_layout.addWidget(self.value_current_cost_sa, 1, 1)
        sa_layout.addWidget(self.value_relative_error_current_sa, 1, 2)

        # Row 3: Best Cost and Error for SA
        sa_layout.addWidget(self.create_label("Best Cost / Error:"), 2, 0)
        self.value_best_cost_sa: QLineEdit = self.create_line_edit("0", width=80)
        self.value_relative_error_best_sa: QLineEdit = self.create_line_edit("0%", width=80)
        sa_layout.addWidget(self.value_best_cost_sa, 2, 1)
        sa_layout.addWidget(self.value_relative_error_best_sa, 2, 2)

        self.sa_group_box.setLayout(sa_layout)

        # Group box for Tabu Search (TS) results
        self.ts_group_box: QGroupBox = QGroupBox("Tabu Search Results")
        self.ts_group_box.setStyleSheet("""
            QGroupBox {
                font-size: 13pt;
            }
        """)
        self.ts_group_box.setFixedWidth(self.fixed_width)
        ts_layout: QGridLayout = QGridLayout()

        # Row 1: Optimal Cost for TS
        ts_layout.addWidget(self.create_label("Optimal Cost:"), 0, 0)
        self.value_optimal_cost_ts: QLineEdit = self.create_line_edit("0", width=80)
        ts_layout.addWidget(self.value_optimal_cost_ts, 0, 1)

        # Row 2: Current Cost and Error for TS
        ts_layout.addWidget(self.create_label("Current Cost / Error:"), 1, 0)
        self.value_current_cost_ts: QLineEdit = self.create_line_edit("0", width=80)
        self.value_relative_error_current_ts: QLineEdit = self.create_line_edit("0%", width=80)
        ts_layout.addWidget(self.value_current_cost_ts, 1, 1)
        ts_layout.addWidget(self.value_relative_error_current_ts, 1, 2)

        # Row 3: Best Cost and Error for TS
        ts_layout.addWidget(self.create_label("Best Cost / Error:"), 2, 0)
        self.value_best_cost_ts: QLineEdit = self.create_line_edit("0", width=80)
        self.value_relative_error_best_ts: QLineEdit = self.create_line_edit("0%", width=80)
        ts_layout.addWidget(self.value_best_cost_ts, 2, 1)
        ts_layout.addWidget(self.value_relative_error_best_ts, 2, 2)

        self.ts_group_box.setLayout(ts_layout)

        # Spacer items for dynamic layout adjustments
        self.vertical_spacer_top: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_spacer_bottom: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontal_spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Set the main layout and initial visibility
        self.setLayout(self.layout)
        self.update_visibility(show_sa=True, show_ts=True)

    def create_label(self, text: str) -> QLabel:
        """
        Creates a QLabel with a specific style.

        :param text: Text displayed on the label.
        :return: Configured QLabel.
        """
        label: QLabel = QLabel(text)
        label.setStyleSheet("QLabel { background: transparent; border: transparent; }")
        return label

    def create_line_edit(self, default_text: str, width: int) -> QLineEdit:
        """
        Creates a QLineEdit with predefined settings.

        :param default_text: Default text displayed in the line edit.
        :param width: Fixed width of the line edit.
        :return: Configured QLineEdit.
        """
        line_edit: QLineEdit = QLineEdit()
        line_edit.setFixedWidth(width)
        line_edit.setText(default_text)
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        return line_edit

    def update_visibility(self, show_sa: bool, show_ts: bool) -> None:
        """
        Adjusts the visibility and layout of the result boxes based on the selected configuration.

        :param show_sa: Boolean indicating whether to show SA results.
        :param show_ts: Boolean indicating whether to show TS results.
        :return: None
        """
        # Clear the layout to dynamically adjust the content
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i)
            if widget:
                self.layout.removeItem(widget) if isinstance(widget, QSpacerItem) else self.layout.removeWidget(
                    widget.widget())

        if show_sa and show_ts:
            # Center two result boxes side-by-side
            self.layout.addItem(self.horizontal_spacer, 0, 0)
            self.layout.addWidget(self.sa_group_box, 0, 1)
            self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 2)
            self.layout.addWidget(self.ts_group_box, 0, 3)
            self.layout.addItem(self.horizontal_spacer, 0, 4)
        elif show_sa:
            # Center the SA result box only
            self.layout.addItem(self.horizontal_spacer, 0, 0)
            self.layout.addWidget(self.sa_group_box, 0, 1)
            self.layout.addItem(self.horizontal_spacer, 0, 2)
        elif show_ts:
            # Center the TS result box only
            self.layout.addItem(self.horizontal_spacer, 0, 0)
            self.layout.addWidget(self.ts_group_box, 0, 1)
            self.layout.addItem(self.horizontal_spacer, 0, 2)

        # Add vertical spacers for visual balance
        self.layout.addItem(self.vertical_spacer_top, 0, 0, 1, 5)
        self.layout.addItem(self.vertical_spacer_bottom, 2, 0, 1, 5)

        self.sa_group_box.setVisible(show_sa)
        self.ts_group_box.setVisible(show_ts)

    def set_optimal_cost(self, optimal_cost: int, algorithm_type: str) -> None:
        """
        Sets the "Optimal Cost" value for a specified algorithm type (SA or TS).

        :param optimal_cost: The best available result for the TSP instance.
        :param algorithm_type: The algorithm type ("SA" or "TS").
        :return: None
        """
        optimal_cost_text = str(optimal_cost) if optimal_cost is not None else "N/A"
        if algorithm_type == "SA":
            self.value_optimal_cost_sa.setText(optimal_cost_text)
        elif algorithm_type == "TS":
            self.value_optimal_cost_ts.setText(optimal_cost_text)

    def update_sa_results(self, best_cost: int, current_cost: int) -> None:
        """
        Updates the results for the Simulated Annealing (SA) algorithm.

        :param best_cost: Best cost found by the SA algorithm.
        :param current_cost: Current cost in the SA algorithm.
        :return: None
        """
        self.value_best_cost_sa.setText(str(best_cost))
        self.value_current_cost_sa.setText(str(current_cost))
        optimal_cost_text = self.value_optimal_cost_sa.text()
        if optimal_cost_text != "N/A":
            optimal_cost = int(optimal_cost_text)
            current_error = self.calculate_relative_error(current_cost, optimal_cost)
            best_error = self.calculate_relative_error(best_cost, optimal_cost)
            self.value_relative_error_current_sa.setText(f"{current_error:.2f}%")
            self.value_relative_error_best_sa.setText(f"{best_error:.2f}%")

    def update_ts_results(self, best_cost: int, current_cost: int) -> None:
        """
        Updates the results for the Tabu Search (TS) algorithm.

        :param best_cost: Best cost found by the TS algorithm.
        :param current_cost: Current cost in the TS algorithm.
        :return: None
        """
        self.value_best_cost_ts.setText(str(best_cost))
        self.value_current_cost_ts.setText(str(current_cost))
        optimal_cost_text = self.value_optimal_cost_ts.text()
        if optimal_cost_text != "N/A":
            optimal_cost = int(optimal_cost_text)
            current_error = self.calculate_relative_error(current_cost, optimal_cost)
            best_error = self.calculate_relative_error(best_cost, optimal_cost)
            self.value_relative_error_current_ts.setText(f"{current_error:.2f}%")
            self.value_relative_error_best_ts.setText(f"{best_error:.2f}%")

    def clear_results_partially(self) -> None:
        """
        Clears all results except for the optimal cost values.

        :return: None
        """
        self.value_current_cost_sa.setText("0")
        self.value_relative_error_current_sa.setText("0%")
        self.value_best_cost_sa.setText("0")
        self.value_relative_error_best_sa.setText("0%")

        self.value_current_cost_ts.setText("0")
        self.value_relative_error_current_ts.setText("0%")
        self.value_best_cost_ts.setText("0")
        self.value_relative_error_best_ts.setText("0%")

    def clear_results(self) -> None:
        """
        Clears all results, including the optimal cost values.

        :return: None
        """
        self.clear_results_partially()
        self.value_optimal_cost_sa.setText("0")
        self.value_optimal_cost_ts.setText("0")

    @staticmethod
    def calculate_relative_error(current_cost: int, optimal_cost: int) -> float:
        """
        Calculates the relative error between the current and optimal cost.

        :param current_cost: The current cost found by the algorithm.
        :param optimal_cost: The optimal (best known) cost for the TSP instance.
        :return: Relative error as a percentage.
        """
        return ((current_cost - optimal_cost) / optimal_cost) * 100 if optimal_cost > 0 else 0
