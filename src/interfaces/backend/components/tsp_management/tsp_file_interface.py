# src/interfaces/backend/components/tsp_management/tsp_file_interface.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class TSPFileInterface(ABC):
    @abstractmethod
    def load_metadata(self) -> None:
        """Load metadata from the .tsp file."""
        pass

    @abstractmethod
    def load_optimal_results(self) -> None:
        """
        Loads metadata from the .tsp file using the injected TSPLIBParser.
        Checks if the edge weight type is EXPLICIT and automatically loads the distance matrix if it is.
        """
        pass

    @abstractmethod
    def load_display_coordinates(self) -> None:
        """Loads coordinates from the DISPLAY_DATA_SECTION for visualization."""
        pass

    @abstractmethod
    def load_distance_matrix(self) -> None:
        """Loads the distance matrix from the file if not already loaded."""
        pass

    @abstractmethod
    def get_distance_matrix(self) -> Optional[List[List[int]]]:
        """Get the distance matrix if it's already loaded."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Exports the TSPFile data as a dictionary."""
        pass
