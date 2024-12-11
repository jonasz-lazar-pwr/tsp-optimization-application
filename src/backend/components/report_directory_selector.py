# src/backend/components/report_directory_selector.py

import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog

from src.utils.path_config import get_path


class ReportDirectorySelector:
    def __init__(self, output_directory: str) -> None:
        """
        Initializes the ReportDirectorySelector with the specified directory path
        for storing generated reports.

        :param output_directory: The relative path to the default directory for saving reports.
        :return: None
        """
        self.output_directory: str = get_path(output_directory)

    def generate_default_report_name(self, file_name: str) -> str:
        """
        Generates a default name for the report file based on the current date.

        :param file_name: The base name of the TSP instance for the report.
        :return: A string containing the generated report name in the format "TSP_Report_{file_name}_{YYYYMMDD}".
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        report_name = f"TSP_Report_{file_name}_{timestamp}"
        return report_name

    def select_report_path(self, default_file_name: str) -> str:
        """
        Opens a file dialog to select a save path and file name for the report.
        Returns the selected path or an empty string if the user cancels.

        :param default_file_name: The default name for the report file.
        :return: The full file path selected by the user or an empty string if canceled.
        """
        default_path = os.path.join(self.output_directory, default_file_name)
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Report As",
            default_path,
            "PDF Files (*.pdf)"
        )

        # Usuń dodatkowe rozszerzenie ".pdf" jeśli zostało dodane dwukrotnie
        if save_path.endswith(".pdf.pdf"):
            save_path = save_path[:-4]
        return save_path
