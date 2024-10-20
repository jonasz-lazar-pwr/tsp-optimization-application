# src/interfaces/backend/components/tsp_management/tsp_catalog_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional

from src.backend.components.tsp_management.tsp_file import TSPFile


class TSPCatalogInterface(ABC):
    @abstractmethod
    def load_files(self, directory_path: str) -> None:
        """Loads .tsp files from the specified directory and stores them in the catalog."""
        pass

    @abstractmethod
    def get_file_by_name(self, name: str) -> Optional[TSPFile]:
        """Retrieves a TSP file by its name from the catalog."""
        pass

    @abstractmethod
    def sort_by_dimension(self) -> None:
        """Sorts the TSP files in the catalog by the number of cities (dimension)."""
        pass

    @abstractmethod
    def filter_by_edge_weight_type(self, edge_weight_type: str) -> List[TSPFile]:
        """Filters TSP files by the specified edge weight type."""
        pass

    @abstractmethod
    def load_distance_matrix_for_file(self, name: str) -> Optional[TSPFile]:
        """Loads the distance matrix for a specified TSP file by its name."""
        pass