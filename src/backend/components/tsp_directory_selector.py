# src/backend/components/tsp_directory_selector.py

from PySide6.QtWidgets import QFileDialog

from src.utils.path_config import get_path
from src.backend.tsp_management.tsp_catalog import TSPCatalog


class TSPDirectorySelector:
    def __init__(self, catalog: TSPCatalog) -> None:
        """
        Initializes the TSPDirectorySelector with a TSPCatalog instance for loading .tsp files.

        :param catalog: The TSPCatalog instance responsible for managing TSP files.
        :return: None
        """
        self.catalog: TSPCatalog = catalog  # Injected TSPCatalog

    def select_directory_and_load_files(self) -> None:
        """
        Opens a directory selection dialog and loads .tsp files from the selected directory into the catalog.
        Clears previously loaded files in the catalog before loading new files.

        :return: None
        """
        file_dialog: QFileDialog = QFileDialog()

        # Set default directory to 'data/tsplib'
        default_directory: str = get_path('data/tsplib')
        file_dialog.setDirectory(default_directory)

        # Configure dialog to show directories only
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        # Load .tsp files if a directory is selected
        if file_dialog.exec():
            selected_directory: str = file_dialog.selectedFiles()[0]
            # Clear any previously loaded files in the catalog
            self.catalog.clear_files()

            # Load files from the selected directory into the catalog
            self.catalog.load_files(selected_directory)