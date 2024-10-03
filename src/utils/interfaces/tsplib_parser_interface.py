# src/utils/interfaces/tsplib_parser_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class TSPLIBParserInterface(ABC):
    @abstractmethod
    def validate_file(self, file_path: str) -> None:
        """Validate if the file exists and has the correct structure."""
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
    def get_field_value(self, field_name: str, optional: bool = False) -> Optional[str]:
        """Get the value of a specified field from the file content."""
        pass

    @abstractmethod
    def get_distance_matrix(self) -> List[List[int]]:
        """Return the generated distance matrix."""
        pass
