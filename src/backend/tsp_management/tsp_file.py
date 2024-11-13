# src/backend/tsp_management/tsp_file.py

import os
import json
from typing import Optional, List, Dict, Tuple
from src.backend.tsp_management.tsplib_parser import TSPLIBParser


class TSPFile:
    def __init__(self, file_path:  str, optimal_results_path: str, parser: TSPLIBParser) -> None:
        """
        Initializes a TSPFile instance, representing a Traveling Salesman Problem instance with metadata and distance
        information.

        :param file_path: Path to the .tsp file.
        :param optimal_results_path: Path to the JSON file containing optimal results.
        :param parser: Instance of TSPLIBParser injected through constructor.
        """
        self.file_path: str = file_path
        self.name: Optional[str] = None
        self.type: Optional[str] = None
        self.dimension: Optional[int] = None
        self.edge_weight_type: Optional[str] = None
        self.edge_weight_format: Optional[str] = None
        self.coordinates: List[Tuple[float, float]] = []
        self.display_coordinates: List[Tuple[float, float]] = []
        self.distance_matrix: List[List[int]] = []
        self.has_loaded: bool = False
        self.optimal_result: Optional[int] = None
        self.optimal_results_path: str = optimal_results_path
        self.parser: TSPLIBParser = parser

    def load_metadata(self) -> None:
        """
        Loads metadata from the .tsp file using the injected TSPLIBParser. If the edge weight type is "EXPLICIT",
        the distance matrix is loaded automatically. Also loads display coordinates if available.

        :return: None
        """
        self.parser.validate_file(self.file_path)
        self.name = self.parser.get_field_value("NAME")
        self.type = self.parser.get_field_value("TYPE")
        self.dimension = int(self.parser.get_field_value("DIMENSION"))
        self.edge_weight_type = self.parser.get_field_value("EDGE_WEIGHT_TYPE")
        self.edge_weight_format = self.parser.get_field_value("EDGE_WEIGHT_FORMAT", optional=True)
        self.load_optimal_results()

        # Load display coordinates only if the file has DISPLAY_DATA_SECTION
        if self.edge_weight_type != "EXPLICIT":
            self.coordinates = self.parser.coordinates

        # Load distance matrix if the file has EDGE_WEIGHT_SECTION
        if self.edge_weight_type == "EXPLICIT":
            self.load_distance_matrix()

        # Load display coordinates if the file has DISPLAY_DATA_SECTION
        display_data_type = self.parser.get_field_value("DISPLAY_DATA_TYPE", optional=True)
        if display_data_type == "TWOD_DISPLAY":
            self.load_display_coordinates()

    def load_optimal_results(self) -> None:
        """
        Loads the optimal result for the problem from a local JSON file, handling errors appropriately.
        If the JSON file does not contain optimal data for this instance, sets optimal_result to None.

        :return: None
        :raises FileNotFoundError: If the optimal results file cannot be found.
        :raises json.JSONDecodeError: If the JSON file is improperly formatted.
        :raises ValueError: If the JSON content does not match the expected structure.
        """
        try:
            # Ensure the JSON file exists
            if not self.optimal_results_path or not os.path.exists(self.optimal_results_path):
                raise FileNotFoundError(f"Optimal results JSON file not found: {self.optimal_results_path}")

            # Load the JSON file
            with open(self.optimal_results_path, 'r') as json_file:
                optimal_data = json.load(json_file)

            # Validate that the loaded data is a dictionary
            if not isinstance(optimal_data, dict):
                raise ValueError(f"Invalid JSON format in {self.optimal_results_path}. Expected a dictionary.")

            # Fetch the optimal length for the current TSP file, without changing case
            file_key = os.path.basename(self.file_path).replace('.tsp', '')

            # Retrieving the optimal length based on the file key
            self.optimal_result = optimal_data.get(file_key, None)

        except FileNotFoundError as fnf_error:
            print(f"Error: {fnf_error}")
            self.optimal_result = None

        except json.JSONDecodeError as json_error:
            print(f"Error decoding JSON: {json_error}")
            self.optimal_result = None

        except ValueError as val_error:
            print(f"Validation error in JSON file: {val_error}")
            self.optimal_result = None

    def load_display_coordinates(self) -> None:
        """
        Loads coordinates from the DISPLAY_DATA_SECTION for visualization purposes.

        :return: None
        """
        self.display_coordinates = self.parser.load_display_coordinates()

    def load_distance_matrix(self) -> None:
        """
        Loads the distance matrix using the parser if it has not already been loaded.

        :return: None
        """
        if not self.has_loaded:
            self.parser.generate_distance_matrix()
            self.distance_matrix = self.parser.get_distance_matrix()
            self.has_loaded = True
        else:
            print("Distance matrix already loaded.")

    def get_distance_matrix(self) -> Optional[List[List[int]]]:
        """
        Retrieves the distance matrix if it has been loaded.

        :return: The distance matrix or None if it hasn't been loaded yet.
        """
        if self.has_loaded:
            return self.distance_matrix
        else:
            print("Distance matrix not loaded yet.")
            return None

    def to_dict(self) -> Dict:
        """
        Exports the TSPFile data as a dictionary.

        :return: A dictionary containing the file's metadata, coordinates, and distance matrix.
        """
        return {
            'file_path': self.file_path,
            'name': self.name,
            'type': self.type,
            'dimension': self.dimension,
            'edge_weight_type': self.edge_weight_type,
            'edge_weight_format': self.edge_weight_format,
            'optimal_length': self.optimal_result,
            'coordinates': self.coordinates,
            'display_coordinates': self.display_coordinates,
            'distance_matrix': self.distance_matrix if self.has_loaded else None,
            'has_loaded': self.has_loaded,
            'optimal_results_path': self.optimal_results_path,
        }
