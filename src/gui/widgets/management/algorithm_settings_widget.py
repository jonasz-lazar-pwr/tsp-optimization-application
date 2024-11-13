# src/gui/widgets/management/algorithm_settings_widget.py

from typing import Optional
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGroupBox, QSizePolicy, QSpacerItem

from src.gui.widgets.management.sa_settings_widget import SASettingsWidget
from src.gui.widgets.management.ts_settings_widget import TSSettingsWidget


class AlgorithmSettingsWidget(QWidget):
    # Signal emitted to start the algorithm with the specified parameters.
    run_algorithm_signal = Signal(list)
    # Signal emitted to stop the algorithm.
    stop_algorithm_signal = Signal()

    def __init__(self, algorithm_type: str, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the AlgorithmSettingsWidget, configuring scroll area with specific algorithm settings.

        :param algorithm_type: The type of algorithm ("SA", "TS", or "SA + TS") for which to display settings.
        :param parent: Optional parent widget.
        :return: None
        """
        super().__init__(parent)
        self.algorithm_type: str = algorithm_type

        # Main layout setup
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Scroll area content setup
        scroll_area: QScrollArea = self.setup_scroll_area_content()
        self.layout.addWidget(scroll_area)

        # Assign layout
        self.setLayout(self.layout)

    def setup_scroll_area_content(self) -> QScrollArea:
        """
        Creates and configures the scroll area content, adding SA or TS settings based on algorithm type.

        :return: Configured QScrollArea with algorithm settings content.
        """
        # Configure the scroll area
        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create the scrollable content
        scroll_content: QWidget = QWidget()
        scroll_content.setObjectName("scrollContent")
        scroll_content.setStyleSheet("""
            #scrollContent {
                background-color: #424242;
                border-radius: 0px;
            }
        """)

        scroll_content_layout: QVBoxLayout = QVBoxLayout(scroll_content)
        scroll_content_layout.setAlignment(Qt.AlignTop)  # Align frames to the top

        # Add SA and/or TS settings based on the algorithm type
        self.add_algorithm_sections(scroll_content_layout)

        # Spacer item to push buttons to the bottom
        scroll_content_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Assign the scrollable content to the scroll area
        scroll_area.setWidget(scroll_content)
        return scroll_area

    def add_algorithm_sections(self, layout: QVBoxLayout) -> None:
        """
        Adds SA and/or TS sections to the layout based on the specified algorithm type.

        :param layout: The layout to which the sections will be added.
        :return: None
        """
        if self.algorithm_type in ["SA", "SA + TS"]:
            # Add SA section with a spacer above
            layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

            sa_group_box = QGroupBox("Simulated Annealing Settings")
            sa_group_box.setStyleSheet("""
                QGroupBox {
                    font-size: 13pt;
                }
            """)
            sa_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sa_layout = QVBoxLayout(sa_group_box)
            sa_layout.setContentsMargins(0, 0, 0, 0)
            self.sa_settings_widget: SASettingsWidget = SASettingsWidget()
            sa_layout.addWidget(self.sa_settings_widget)
            layout.addWidget(sa_group_box)

        if self.algorithm_type in ["TS", "SA + TS"]:
            # Add TS section with a spacer above
            layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

            ts_group_box = QGroupBox("Tabu Search Settings")
            ts_group_box.setStyleSheet("""
                QGroupBox {
                    font-size: 13pt;
                }
            """)
            ts_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            ts_layout = QVBoxLayout(ts_group_box)
            ts_layout.setContentsMargins(0, 0, 0, 0)
            self.ts_settings_widget: TSSettingsWidget = TSSettingsWidget()
            ts_layout.addWidget(self.ts_settings_widget)
            layout.addWidget(ts_group_box)

    def on_run_button_clicked(self) -> None:
        """
        Handles the "RUN" button click and emits the run_algorithm_signal with the selected algorithm.

        :return: None
        """
        if self.algorithm_type == "SA":
            params = self.sa_settings_widget.collect_sa_parameters()
            if params:
                self.run_algorithm_signal.emit(["SA"])
        elif self.algorithm_type == "TS":
            params = self.ts_settings_widget.collect_ts_parameters()
            if params:
                self.run_algorithm_signal.emit(["TS"])
        elif self.algorithm_type == "SA + TS":
            params_sa = self.sa_settings_widget.collect_sa_parameters()
            params_ts = self.ts_settings_widget.collect_ts_parameters()
            if params_sa and params_ts:
                self.run_algorithm_signal.emit(["SA", "TS"])
