# src/gui/widgets/management/ts_settings_widget.py

from typing import Optional
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QSpinBox, QLabel, QGroupBox, \
    QSizePolicy

from src.backend.components.ts_parameters import TSParameters, TenureTypeTS, TabuListLimitMethodTS, \
    NeighborSelectionMethodTS, InitialSolutionMethodTS


class TSSettingsWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the TSSettingsWidget, setting up fields for configuring Tabu Search parameters.

        :param parent: Optional parent widget.
        """
        super().__init__(parent)
        self.layout: QVBoxLayout = QVBoxLayout(self)

        # Configure layout for TS parameters
        self.setup_ts_settings()

        # Connect signals for dynamic field updates
        self.tabu_list_limit_method_input.currentIndexChanged.connect(self.update_tabu_list_fields)
        self.tenure_type_input.currentIndexChanged.connect(self.update_tenure_fields)

        # Initial visibility settings for dynamic fields
        self.update_tabu_list_fields()
        self.update_tenure_fields()

        self.setLayout(self.layout)

    def setup_ts_settings(self) -> None:
        """
        Configures the layout for Tabu Search (TS) settings, including general parameters, neighborhood settings,
        tabu list configuration, and tenure fields.

        :return: None
        """
        ts_grid_layout: QGridLayout = QGridLayout()

        # General settings
        self.duration_input: QLineEdit = self.create_line_edit("1", 120, r"^(?!0\d)(\d{1,3})(\.\d{1,3})?$")
        ts_grid_layout.addWidget(self.create_label("Max duration [s]:"), 0, 0)
        ts_grid_layout.addWidget(self.duration_input, 0, 1)

        # Neighborhood and initial solution settings
        self.initial_solution_method_input: QComboBox = self.create_combo_box(
            [solution.value for solution in InitialSolutionMethodTS])
        ts_grid_layout.addWidget(self.create_label("Initial solution method:"), 1, 0)
        ts_grid_layout.addWidget(self.initial_solution_method_input, 1, 1)

        self.neighbor_selection_method_input: QComboBox = self.create_combo_box(
            [move.value for move in NeighborSelectionMethodTS])
        ts_grid_layout.addWidget(self.create_label("Neighbor selection method:"), 2, 0)
        ts_grid_layout.addWidget(self.neighbor_selection_method_input, 2, 1)

        self.max_neighbors_input: QSpinBox = self.create_spin_box(1, 10000, 100, 120, 10)
        ts_grid_layout.addWidget(self.create_label("Max neighbors:"), 3, 0)
        ts_grid_layout.addWidget(self.max_neighbors_input, 3, 1)

        # Tabu List settings
        self.tabu_list_limit_method_input: QComboBox = self.create_combo_box([limit.value for limit in TabuListLimitMethodTS])
        ts_grid_layout.addWidget(self.create_label("Tabu list limit:"), 4, 0)
        ts_grid_layout.addWidget(self.tabu_list_limit_method_input, 4, 1)

        self.tabu_list_custom_limit_input: QSpinBox = self.create_spin_box(1, 10000, 100, 120, 10)
        ts_grid_layout.addWidget(self.create_label("Custom tabu list limit:"), 5, 0)
        ts_grid_layout.addWidget(self.tabu_list_custom_limit_input, 5, 1)

        # Tenure settings
        self.tenure_type_input: QComboBox = self.create_combo_box([tenure.value for tenure in TenureTypeTS])
        ts_grid_layout.addWidget(self.create_label("Tenure type:"), 6, 0)
        ts_grid_layout.addWidget(self.tenure_type_input, 6, 1)

        self.constant_tenure_input: QSpinBox = self.create_spin_box(1, 10000, 100, 120, 10)
        ts_grid_layout.addWidget(self.create_label("Constant tenure:"), 7, 0)
        ts_grid_layout.addWidget(self.constant_tenure_input, 7, 1)

        # Random tenure range group
        self.setup_random_tenure_group(ts_grid_layout)

        # Add main grid layout to TS settings layout
        self.layout.addLayout(ts_grid_layout)

    def setup_random_tenure_group(self, layout: QGridLayout) -> None:
        """
        Configures the random tenure range group, including min and max tenure settings.

        :param layout: The main layout to which the random tenure group will be added.
        :return: None
        """
        random_tenure_group: QGroupBox = QGroupBox()
        random_tenure_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        random_tenure_layout = QVBoxLayout(random_tenure_group)

        # Label for random tenure range
        random_tenure_label: QLabel = self.create_label("Random tenure range:")
        random_tenure_layout.addWidget(random_tenure_label, alignment=Qt.AlignLeft)

        # Min and max values for random tenure range
        random_tenure_range_layout: QGridLayout = QGridLayout()
        self.random_tenure_min_input: QSpinBox = self.create_spin_box(1, 10000, 10, 105, 10)
        random_tenure_range_layout.addWidget(self.create_label("Min:"), 0, 0)
        random_tenure_range_layout.addWidget(self.random_tenure_min_input, 0, 1)

        self.random_tenure_max_input: QSpinBox = self.create_spin_box(1, 10000, 100, 105, 10)
        random_tenure_range_layout.addWidget(self.create_label("Max:"), 1, 0)
        random_tenure_range_layout.addWidget(self.random_tenure_max_input, 1, 1)

        random_tenure_layout.addLayout(random_tenure_range_layout)
        layout.addWidget(random_tenure_group, 8, 0, 1, 2)

    def create_label(self, text: str) -> QLabel:
        """
        Creates and returns a QLabel with specific styling.

        :param text: The text to be displayed on the label.
        :return: Configured QLabel.
        """
        label: QLabel = QLabel(text)
        label.setStyleSheet("QLabel { color: white; background: transparent; border: none; }")
        return label

    def create_line_edit(self, default_text: str, width: int, regex_pattern: str) -> QLineEdit:
        """
        Creates and returns a QLineEdit with specific settings.

        :param default_text: Default text displayed in the line edit.
        :param width: Fixed width of the line edit.
        :param regex_pattern: Regular expression pattern for input validation.
        :return: Configured QLineEdit.
        """
        line_edit: QLineEdit = QLineEdit()
        line_edit.setFixedWidth(width)
        line_edit.setText(default_text)
        line_edit.setAlignment(Qt.AlignCenter)
        validator: QRegularExpressionValidator = QRegularExpressionValidator(QRegularExpression(regex_pattern), line_edit)
        line_edit.setValidator(validator)
        return line_edit

    def create_combo_box(self, items: list[str]) -> QComboBox:
        """
        Creates and returns a QComboBox with specified items.

        :param items: List of items to be added to the combo box.
        :return: Configured QComboBox.
        """
        combo_box: QComboBox = QComboBox()
        combo_box.addItems(items)
        combo_box.setFixedWidth(125)
        return combo_box

    def create_spin_box(self, minimum: int, maximum: int, default_value: int, width: int,
                        single_step: int = 1) -> QSpinBox:
        """
        Creates and returns a QSpinBox with specific settings.

        :param minimum: Minimum value for the spin box.
        :param maximum: Maximum value for the spin box.
        :param default_value: Default value of the spin box.
        :param width: Width of the spin box.
        :param single_step: Step increment for the spin box.
        :return: Configured QSpinBox.
        """
        spin_box: QSpinBox = QSpinBox()
        spin_box.setRange(minimum, maximum)
        spin_box.setValue(default_value)
        spin_box.setSingleStep(single_step)
        spin_box.setMinimumSize(width, 23)
        spin_box.lineEdit().setAlignment(Qt.AlignCenter)
        return spin_box

    def update_tabu_list_fields(self) -> None:
        """
        Updates the editability of the 'Custom tabu list limit' field based on the selected list limit method.

        :return: None
        """
        is_custom: bool = self.tabu_list_limit_method_input.currentText() == "CUSTOM"
        self.tabu_list_custom_limit_input.setEnabled(is_custom)

    def update_tenure_fields(self) -> None:
        """
        Updates the visibility of 'Constant' and 'Random' tenure fields based on the selected tenure type.

        :return: None
        """
        is_constant: bool = self.tenure_type_input.currentText() == "CONSTANT"
        self.constant_tenure_input.setEnabled(is_constant)
        self.random_tenure_min_input.setEnabled(not is_constant)
        self.random_tenure_max_input.setEnabled(not is_constant)

    def collect_ts_parameters(self) -> Optional[TSParameters]:
        """
        Collects and validates parameters for Tabu Search (TS).

        :return: TSParameters instance if valid parameters are collected, otherwise None.
        """
        try:
            duration_ms = int(float(self.duration_input.text()) * 1000)
            initial_solution_method = InitialSolutionMethodTS(self.initial_solution_method_input.currentText())
            neighbor_selection_method = NeighborSelectionMethodTS(self.neighbor_selection_method_input.currentText())
            tenure_type = TenureTypeTS(self.tenure_type_input.currentText())
            constant_tenure = self.constant_tenure_input.value() if tenure_type == TenureTypeTS.CONSTANT else 0
            random_tenure_range = (
                self.random_tenure_min_input.value(),
                self.random_tenure_max_input.value()
            ) if tenure_type == TenureTypeTS.RANDOM else (0, 0)
            tabu_list_limit_method = TabuListLimitMethodTS(self.tabu_list_limit_method_input.currentText())
            tabu_list_custom_limit = self.tabu_list_custom_limit_input.value() if tabu_list_limit_method == TabuListLimitMethodTS.CUSTOM else 0
            max_neighbors = self.max_neighbors_input.value()

            return TSParameters(
                duration_ms=duration_ms,
                tenure_type=tenure_type,
                constant_tenure=constant_tenure,
                random_tenure_range=random_tenure_range,
                tabu_list_limit_method=tabu_list_limit_method,
                tabu_list_custom_limit=tabu_list_custom_limit,
                max_neighbors=max_neighbors,
                neighbor_selection_method=neighbor_selection_method,
                initial_solution_method=initial_solution_method
            )
        except ValueError:
            print("Invalid TS parameters")
            return None
