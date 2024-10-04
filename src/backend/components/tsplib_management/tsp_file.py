# src/backend/components/tsplib_management/tsp_file.py

import json
import os
from typing import Optional, List, Dict

from src.utils.interfaces.tsp_file_interface import TSPFileInterface
from src.backend.components.tsplib_management.tsplib_parser import TSPLIBParser


class TSPFile(TSPFileInterface):
    def __init__(self, file_path:  str, optimal_results_path: str, parser: TSPLIBParser):
        """
        Constructor for the TSPFile class.

        :param file_path: Path to the .tsp file.
        :param optimal_results_path: Path to the JSON file containing optimal results.
        :param parser: Instance of TSPLIBParser injected through constructor.
        """
        self.file_path = file_path
        self.name = None
        self.type = None
        self.dimension = None
        self.edge_weight_type = None
        self.edge_weight_format = None
        self.coordinates = []
        self.display_coordinates = []
        self.distance_matrix = []
        self.has_loaded = False
        self.optimal_result = None
        self.optimal_results_path = optimal_results_path
        self.parser = parser

    def load_metadata(self) -> None:
        """
        Load metadata from the .tsp file using the injected TSPLIBParser.
        It loads the metadata and checks if the edge weight type is EXPLICIT.
        If it is, it will automatically load the distance matrix.
        """
        print("Loading metadata...")
        self.parser.validate_file(self.file_path)
        self.name = self.parser.get_field_value("NAME")
        self.type = self.parser.get_field_value("TYPE")
        self.dimension = int(self.parser.get_field_value("DIMENSION"))
        self.edge_weight_type = self.parser.get_field_value("EDGE_WEIGHT_TYPE")
        print(f"Metadata loaded with edge_weight_type: {self.edge_weight_type}")
        self.edge_weight_format = self.parser.get_field_value("EDGE_WEIGHT_FORMAT", optional=True)
        self.load_optimal_results()

        # Load display coordinates only if the file has DISPLAY_DATA_SECTION
        if self.edge_weight_type != "EXPLICIT":
            self.coordinates = self.parser.coordinates

        if self.edge_weight_type == "EXPLICIT":
            self.load_distance_matrix()
        print(f"Finished loading metadata for file {self.file_path}. edge_weight_type: {self.edge_weight_type}")

        display_data_type = self.parser.get_field_value("DISPLAY_DATA_TYPE", optional=True)
        if display_data_type == "TWOD_DISPLAY":
            self.load_display_coordinates()

    def load_optimal_results(self) -> None:
        """
        Load the optimal result for the problem from the local JSON file, with error handling.
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

            # Fetch the optimal length for the current TSP file, bez zmiany wielkości liter
            file_key = os.path.basename(self.file_path).replace('.tsp', '')

            # Pobieranie optymalnej długości na podstawie klucza pliku
            self.optimal_result = optimal_data.get(file_key, None)

            if self.optimal_result is None:
                print(f"No optimal result found for {file_key} in {self.optimal_results_path}")

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
        Load coordinates from the DISPLAY_DATA_SECTION for visualization.
        """
        self.display_coordinates = self.parser.load_display_coordinates()

    def load_distance_matrix(self) -> None:
        """
        Load the distance matrix on demand.
        """
        if not self.has_loaded:
            print(f"Generating distance matrix for {self.file_path} with type {self.edge_weight_type}")
            self.parser.generate_distance_matrix()
            self.distance_matrix = self.parser.get_distance_matrix()
            print(f"Distance matrix generated with {len(self.distance_matrix)} cities.")
            self.has_loaded = True
        else:
            print("Distance matrix already loaded.")

    def get_distance_matrix(self) -> Optional[List[List[int]]]:
        """
        Get the distance matrix if it's already loaded.

        :return: The distance matrix or None if it hasn't been loaded yet.
        """
        if self.has_loaded:
            return self.distance_matrix
        else:
            print("Distance matrix not loaded yet.")
            return None

    def to_dict(self) -> Dict:
        """
        Export the file data as a dictionary.

        :return: A dictionary with all relevant file information.
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
