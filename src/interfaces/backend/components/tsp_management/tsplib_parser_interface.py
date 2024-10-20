# src/interfaces/backend/components/tsp_management/tsplib_parser_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class TSPLIBParserInterface(ABC):
    @abstractmethod
    def validate_file(self, file_path: str) -> None:
        """Validate if the file exists and has the correct structure."""
        pass

    @abstractmethod
    def _load_coordinates(self) -> None:
        """Load city coordinates from the NODE_COORD_SECTION."""
        pass

    @abstractmethod
    def load_display_coordinates(self) -> List[Tuple[float, float]]:
        """Load coordinates from the DISPLAY_DATA_SECTION if it exists."""
        pass

    @abstractmethod
    def generate_distance_matrix(self) -> None:
        """Generate a distance matrix based on EDGE_WEIGHT_TYPE."""
        pass

    @abstractmethod
    def _calculate_euclidean_distance_2d(self) -> None:
        """Calculate the Euclidean distance between 2D coordinates."""
        pass

    @abstractmethod
    def _calculate_ceil_euclidean_distance_2d(self) -> None:
        """Calculate the Euclidean distance between 2D coordinates and round it up."""
        pass

    @abstractmethod
    def _calculate_att_distance(self) -> None:
        """Calculate the pseudo-Euclidean ATT distance between coordinates."""
        pass

    @abstractmethod
    def _calculate_geographical_distance(self) -> None:
        """Calculate the geographical distance between coordinates."""
        pass

    @abstractmethod
    def _load_explicit_weights(self) -> None:
        """Load the explicit edge weights based on the format from the EDGE_WEIGHT_SECTION."""
        pass

    @abstractmethod
    def _load_full_matrix(self, values: List[int], dimension: int) -> None:
        """Load the full matrix of edge weights."""
        pass

    @abstractmethod
    def _load_triangular(self, values: List[int], dimension: int, lower: bool, diag: bool) -> None:
        """Load a triangular matrix, with or without the diagonal."""
        pass

    @abstractmethod
    def _convert_matrix_to_integers(self) -> None:
        """Convert all values in the distance matrix to integers."""
        pass

    @abstractmethod
    def _unsupported_format(self) -> None:
        """Raise an exception for an unsupported format."""
        pass

    @abstractmethod
    def get_field_value(self, field_name: str, optional: bool = False) -> Optional[str]:
        """Get the value of a specified field from the file content."""
        pass

    @abstractmethod
    def get_distance_matrix(self) -> List[List[int]]:
        """Return the generated distance matrix."""
        pass
