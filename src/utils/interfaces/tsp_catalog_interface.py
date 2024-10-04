# src/utils/interfaces/tsp_catalog_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional

from src.backend.components.tsplib_management.tsp_file import TSPFile


class TSPCatalogInterface(ABC):
    @abstractmethod
    def load_files(self, directory_path: str) -> None:
        """Load .tsp files from the specified directory."""
        pass

    @abstractmethod
    def get_file_by_name(self, name: str) -> Optional[TSPFile]:
        """Find a TSP file by its name."""
        pass

    @abstractmethod
    def sort_by_dimension(self) -> None:
        """Sort files by the number of cities (dimension)."""
        pass

    @abstractmethod
    def filter_by_edge_weight_type(self, edge_weight_type: str) -> List[TSPFile]:
        """Filter files by the edge weight type."""
        pass

    @abstractmethod
    def load_distance_matrix_for_file(self, name: str) -> Optional[TSPFile]:
        """Load the distance matrix for a specific file by its name."""
        pass