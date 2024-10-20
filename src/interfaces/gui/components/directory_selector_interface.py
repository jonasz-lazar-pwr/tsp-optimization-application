# src/interfaces/gui/components/directory_selector_interface.py

from abc import ABC, abstractmethod


class DirectorySelectorInterface(ABC):
    @abstractmethod
    def select_directory_and_load_files(self) -> None:
        """Opens a dialog to select a directory and automatically loads the .tsp files within it."""
        pass
