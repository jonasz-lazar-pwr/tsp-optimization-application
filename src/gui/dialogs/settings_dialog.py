# src/gui/dialogs/settings_dialog.py

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QWidget
from PySide6.QtGui import QIntValidator


class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget = None) -> None:
        """
        Initializes the settings dialog for configuring ports and data transmission frequency.

        :param parent: The parent widget for this dialog.
        """
        super().__init__(parent)
        self.setWindowTitle("Settings")

        # Main layout setup
        layout: QVBoxLayout = QVBoxLayout(self)

        # Form layout for settings fields
        form_layout: QFormLayout = QFormLayout()

        # Validator for port fields (valid range: 1024 - 65535)
        port_validator: QIntValidator = QIntValidator(1024, 65535, self)

        # Ports configuration for SA and TS algorithms
        self.sa_port_input: QLineEdit = QLineEdit()
        self.sa_port_input.setValidator(port_validator)
        self.sa_port_input.setText("5555")  # Default SA port
        self.sa_port_input.setAlignment(Qt.AlignCenter)

        self.ts_port_input: QLineEdit = QLineEdit()
        self.ts_port_input.setValidator(port_validator)
        self.ts_port_input.setText("6666")  # Default TS port
        self.ts_port_input.setAlignment(Qt.AlignCenter)

        # Validator for frequency field (positive integers only, optional upper limit of 1000000 ms)
        frequency_validator: QIntValidator = QIntValidator(1, 1000000, self)

        # Data transmission frequency input
        self.data_frequency_input: QLineEdit = QLineEdit()
        self.data_frequency_input.setValidator(frequency_validator)
        self.data_frequency_input.setText("1")  # Default frequency in milliseconds
        self.data_frequency_input.setAlignment(Qt.AlignCenter)

        # Label styling for consistency
        label_style: str = "QLabel { color: white; background: transparent; border: none; }"

        # Configure and add labels and input fields to form layout
        sa_port_label: QLabel = QLabel("SA data transmission port:")
        sa_port_label.setStyleSheet(label_style)
        form_layout.addRow(sa_port_label, self.sa_port_input)

        ts_port_label: QLabel = QLabel("TS data transmission port:")
        ts_port_label.setStyleSheet(label_style)
        form_layout.addRow(ts_port_label, self.ts_port_input)

        data_frequency_label: QLabel = QLabel("Data transmission frequency [ms]:")
        data_frequency_label.setStyleSheet(label_style)
        form_layout.addRow(data_frequency_label, self.data_frequency_input)

        # Add form layout to main layout
        layout.addLayout(form_layout)

        # Save button setup
        save_button: QPushButton = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

    def save_settings(self) -> None:
        """
        Validates and saves the settings for SA and TS ports and data transmission frequency.

        :return: None
        """
        try:
            # Retrieve and validate port values
            sa_port: int = int(self.sa_port_input.text())
            ts_port: int = int(self.ts_port_input.text())
            data_frequency: int = int(self.data_frequency_input.text())

            # Validate that ports are distinct and within range
            if sa_port == ts_port:
                print("Validation Error: Ports for SA and TS must be different.")
                return
            if not (1024 <= sa_port <= 65535) or not (1024 <= ts_port <= 65535):
                print("Validation Error: Ports must be in the range 1024-65535.")
                return

            # Validate that data frequency is a positive integer
            if data_frequency <= 0:
                print("Validation Error: Data frequency must be a positive integer.")
                return

            # Save settings
            self.accept()

        except ValueError:
            print("Validation Error: Please enter valid integer values for the ports and frequency.")
