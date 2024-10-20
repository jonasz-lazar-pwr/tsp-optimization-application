# src/gui/components/directory_selector.py

from PySide6.QtWidgets import QFileDialog

from src.utils.path_config import get_path
from src.interfaces.gui.components.directory_selector_interface import DirectorySelectorInterface
from src.backend.components.tsp_management.tsp_catalog import TSPCatalog


class DirectorySelector(DirectorySelectorInterface):
    def __init__(self, catalog: TSPCatalog) -> None:
        """
        Constructor that accepts a TSPCatalog instance as a dependency.

        :param catalog: The TSPCatalog instance used to load .tsp files.
        """
        self.catalog = catalog  # Injected TSPCatalog

    def select_directory_and_load_files(self) -> None:
        """
        Opens a dialog to select a directory and automatically loads the .tsp files within it.

        :return: None
        """
        file_dialog = QFileDialog()

        # Set the default path to the 'resources/tsplib' directory
        default_directory = get_path('resources/tsplib')
        file_dialog.setDirectory(default_directory)

        # Set the file mode to select directories only
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)  # Show only directories

        # If the user selects a directory, load the .tsp files from it
        if file_dialog.exec():
            selected_directory = file_dialog.selectedFiles()[0]
            print(f"Selected directory: {selected_directory}")

            # Automatically load the files after selecting a directory
            self.catalog.load_files(selected_directory)