# src/backend/components/tsp_management/tsp_catalog.py

import os
from typing import Optional, List

from src.backend.components.tsp_management.tsplib_parser import TSPLIBParser
from src.backend.components.tsp_management.tsp_file import TSPFile
from src.interfaces.backend.components.tsp_management.tsp_catalog_interface import TSPCatalogInterface


class TSPCatalog(TSPCatalogInterface):
    def __init__(self, optimal_results_path: str) -> None:
        """
        Initializes the TSPCatalog class, which manages a collection of TSP files.

        :param optimal_results_path: Path to the JSON file containing optimal results for all problems.
        :return: None
        """
        self.tsp_files = []
        self.optimal_results_path = optimal_results_path

    def load_files(self, directory_path: str) -> None:
        """
        Loads .tsp files from the specified directory and stores them in the catalog.

        :param directory_path: Path to the directory containing .tsp files.
        :return: None
        """
        for filename in os.listdir(directory_path):
            if filename.endswith(".tsp"):
                try:
                    file_path = os.path.join(directory_path, filename)
                    # Tworzenie nowego parsera dla każdego pliku
                    parser = TSPLIBParser()
                    tsp_file = TSPFile(file_path, self.optimal_results_path, parser)
                    tsp_file.load_metadata()  # Load only metadata
                    self.tsp_files.append(tsp_file)
                except Exception as e:
                    print(f"Error loading file {filename}: {e}")

    def print_all_metadata(self) -> None:
        """
        Prints metadata for all loaded TSP files in the catalog.

        :return: None
        """
        for tsp_file in self.tsp_files:
            print(f"Metadata for file {tsp_file.name}:")
            metadata = tsp_file.to_dict()
            for key, value in metadata.items():
                print(f"{key}: {value}")
            print("-" * 40)

    def get_file_by_name(self, name: str) -> Optional[TSPFile]:
        """
        Retrieves a TSP file by its name from the catalog.

        :param name: The name of the .tsp file.
        :return: The corresponding TSPFile object, or None if not found.
        """
        for tsp_file in self.tsp_files:
            if tsp_file.name == name:
                return tsp_file
        return None

    def sort_by_dimension(self) -> None:
        """
        Sorts the TSP files in the catalog by the number of cities (dimension).

        :return: None
        """
        self.tsp_files.sort(key=lambda file: file.dimension)

    def filter_by_edge_weight_type(self, edge_weight_type: str) -> List[TSPFile]:
        """
        Filters TSP files by the specified edge weight type.

        :param edge_weight_type: The edge weight type to filter by.
        :return: A list of TSPFile objects with the specified edge weight type.
        """
        return [file for file in self.tsp_files if file.edge_weight_type == edge_weight_type]

    def load_distance_matrix_for_file(self, name: str) -> Optional[TSPFile]:
        """
        Loads the distance matrix for a specified TSP file by its name.

        :param name: The name of the .tsp file.
        :return: The TSPFile object with the loaded distance matrix, or None if not found.
        """
        tsp_file = self.get_file_by_name(name)
        if tsp_file:
            tsp_file.load_distance_matrix()
        return tsp_file
