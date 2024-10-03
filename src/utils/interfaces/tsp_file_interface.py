# src/utils/interfaces/tsp_file_interface.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class TSPFileInterface(ABC):
    @abstractmethod
    def load_metadata(self) -> None:
        """Load metadata from the .tsp file."""
        pass

    @abstractmethod
    def load_optimal_results(self) -> None:
        """Load the optimal result for the problem from the local JSON file."""
        pass

    @abstractmethod
    def load_display_coordinates(self) -> None:
        """Load coordinates from the DISPLAY_DATA_SECTION for visualization."""
        pass

    @abstractmethod
    def load_distance_matrix(self) -> None:
        """Load the distance matrix on demand."""
        pass

    @abstractmethod
    def get_distance_matrix(self) -> Optional[List[List[int]]]:
        """Get the distance matrix if it's already loaded, otherwise return None."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Export the file data as a dictionary."""
        pass
