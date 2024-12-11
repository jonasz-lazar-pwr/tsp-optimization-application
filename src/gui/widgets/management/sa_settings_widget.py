# src/gui/widgets/management/sa_settings_widget.py

from typing import Optional

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QSpinBox, QSlider, QLabel, \
    QGroupBox, QSizePolicy
from src.backend.components.sa_parameters import SAParameters, InitialTempMethodSA, NeighborSelectionMethodSA, InitialSolutionMethodSA


class SASettingsWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the SASettingsWidget, setting up fields and sliders for configuring Simulated Annealing parameters.

        :param parent: Optional parent widget.
        :return: None
        """
        super().__init__(parent)
        self.layout: QVBoxLayout = QVBoxLayout(self)

        # General SA settings and alpha setup
        self.setup_sa_settings()
        self.setup_alpha_settings()

        # Set main layout
        self.setLayout(self.layout)

    def setup_sa_settings(self) -> None:
        """
        Configures the layout for general SA settings.

        :return: None
        """
        sa_grid_layout: QGridLayout = QGridLayout()  # Grid layout for general settings

        # General settings
        self.duration_input: QLineEdit = self.create_line_edit("1", 120, r"^(?!0\d)(\d{1,3})(\.\d{1,3})?$")
        sa_grid_layout.addWidget(self.create_label("Max duration [s]:"), 0, 0)
        sa_grid_layout.addWidget(self.duration_input, 0, 1)

        self.initial_temp_method_input: QComboBox = self.create_combo_box([temp.value for temp in InitialTempMethodSA])
        sa_grid_layout.addWidget(self.create_label("Initial temperature method:"), 1, 0)
        sa_grid_layout.addWidget(self.initial_temp_method_input, 1, 1)

        self.initial_solution_method_input: QComboBox = self.create_combo_box([solution.value for solution in InitialSolutionMethodSA])
        sa_grid_layout.addWidget(self.create_label("Initial solution method:"), 2, 0)
        sa_grid_layout.addWidget(self.initial_solution_method_input, 2, 1)

        self.neighbor_selection_method_input: QComboBox = self.create_combo_box([move.value for move in NeighborSelectionMethodSA])
        sa_grid_layout.addWidget(self.create_label("Neighbor selection method:"), 3, 0)
        sa_grid_layout.addWidget(self.neighbor_selection_method_input, 3, 1)

        self.steps_per_temp_input: QSpinBox = self.create_spin_box(1, 100000, 2000, 120, 100)
        sa_grid_layout.addWidget(self.create_label("Steps per temperature:"), 4, 0)
        sa_grid_layout.addWidget(self.steps_per_temp_input, 4, 1)

        # Add grid layout to the main layout
        self.layout.addLayout(sa_grid_layout)


    def setup_alpha_settings(self) -> None:
        """
        Configures the layout for the alpha parameter, including the slider.

        :return: None
        """
        self.alpha_input: QLineEdit = self.create_line_edit("0.500", 105, r"^0\.\d{1,3}$")
        self.alpha_slider: QSlider = self.create_alpha_slider()

        # Group box for alpha settings
        alpha_group: QGroupBox = QGroupBox()
        alpha_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        alpha_layout: QVBoxLayout = QVBoxLayout(alpha_group)

        # Label and input for alpha
        alpha_label_layout: QGridLayout = QGridLayout()
        alpha_label_layout.addWidget(self.create_label("Alpha parameter:"), 0, 0)
        alpha_label_layout.addWidget(self.alpha_input, 0, 1)

        # Add components to the alpha group layout
        alpha_layout.addLayout(alpha_label_layout)
        alpha_layout.addWidget(self.alpha_slider)

        # Center the alpha group in the main layout
        centered_layout: QVBoxLayout = QVBoxLayout()
        centered_layout.addWidget(alpha_group)
        self.layout.addLayout(centered_layout)

    def create_alpha_slider(self) -> QSlider:
        """
        Creates a slider for adjusting the alpha parameter.

        :return: Configured QSlider for the alpha parameter.
        """
        slider: QSlider = QSlider(Qt.Horizontal)
        slider.setRange(1, 999)
        slider.setValue(500)
        slider.valueChanged.connect(self.update_alpha_input_from_slider)
        self.alpha_input.textChanged.connect(self.update_alpha_slider_from_input)
        return slider

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

    def create_spin_box(self, minimum: int, maximum: int, default_value: int, width: int, single_step: int = 1) -> QSpinBox:
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

    def update_alpha_input_from_slider(self) -> None:
        """
        Updates the alpha input value based on the slider position.

        :return: None
        """
        alpha_value: float = self.alpha_slider.value() / 1000
        self.alpha_input.setText(f"{alpha_value:.3f}")


    def update_alpha_slider_from_input(self) -> None:
        """
        Updates the slider position based on the value in the alpha input field.

        :return: None
        """
        if self.alpha_input.hasAcceptableInput() and len(self.alpha_input.text()) == 5:
            try:
                alpha_value = float(self.alpha_input.text())
                if 0.001 <= alpha_value <= 0.999:
                    slider_value = int(alpha_value * 1000)
                    self.alpha_slider.setValue(slider_value)
            except ValueError:
                pass


    def collect_sa_parameters(self) -> Optional[SAParameters]:
        """
        Collects and returns the SA parameters as an SAParameters object if valid, otherwise returns None.

        :return: SAParameters object with collected parameters or None if validation fails.
        """
        try:
            duration_s = float(self.duration_input.text())
            duration_ms = int(duration_s * 1000)
            initial_temp_method = InitialTempMethodSA(self.initial_temp_method_input.currentText())
            alpha = float(self.alpha_input.text())
            steps_per_temp = self.steps_per_temp_input.value()
            neighbor_selection_method = NeighborSelectionMethodSA(self.neighbor_selection_method_input.currentText())
            initial_solution_method = InitialSolutionMethodSA(self.initial_solution_method_input.currentText())

            return SAParameters(
                duration_ms=duration_ms,
                initial_temp_method=initial_temp_method,
                alpha=alpha,
                steps_per_temp=steps_per_temp,
                neighbor_selection_method=neighbor_selection_method,
                initial_solution_method=initial_solution_method
            )
        except ValueError:
            print("Invalid SA parameter values provided.")
            return None
