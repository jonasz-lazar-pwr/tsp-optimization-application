# src/backend/tsp_management/tsp_catalog.py

import os
from typing import Optional, List

from src.backend.tsp_management.tsplib_parser import TSPLIBParser
from src.backend.tsp_management.tsp_file import TSPFile


class TSPCatalog:
    def __init__(self, optimal_results_path: str) -> None:
        """
        Initializes the TSPCatalog class, which manages a collection of TSP files.

        :param optimal_results_path: Path to the JSON file containing optimal results for all problems.
        :return: None
        """
        self.tsp_files: List[TSPFile] = []  # List to store loaded TSP files
        self.optimal_results_path: str = optimal_results_path  # Path to optimal results file

    def clear_files(self) -> None:
        """
        Clears the list of loaded TSP files.

        :return: None
        """
        self.tsp_files.clear()

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
                    parser = TSPLIBParser() # Create a new parser for each file
                    tsp_file = TSPFile(file_path, self.optimal_results_path, parser)
                    tsp_file.load_metadata()  # Load only metadata
                    self.tsp_files.append(tsp_file)
                except Exception as e:
                    print(f"Error loading file {filename}: {e}")

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
