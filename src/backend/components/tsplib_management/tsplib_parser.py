# src/backend/components/tsplib_management/tsp_parser.py

import os
import math
from typing import List, Tuple

from src.utils.interfaces.tsplib_parser_interface import TSPLIBParserInterface


class TSPLIBParser(TSPLIBParserInterface):
    def __init__(self):
        """Constructor."""
        self.file_path = None  # Path to the file
        self.coordinates = []  # List of city coordinates
        self.distance_matrix = []  # Distance matrix
        self.edge_weight_type = None  # Distance type
        self.edge_weight_format = None  # Distance format
        self.content = None

    def validate_file(self, file_path: str) -> None:
        """
        Validate if the file exists and has the correct structure.

        :param file_path: Path to the .tsp file to validate.
        :raises FileNotFoundError: If the file is not found.
        :raises ValueError: If required fields are missing or EDGE_WEIGHT_TYPE is unsupported.
        """
        self.file_path = file_path
        required_fields = ["NAME", "TYPE", "DIMENSION", "EDGE_WEIGHT_TYPE"]

        # Supported EDGE_WEIGHT_TYPE values
        supported_types = ["EXPLICIT", "EUC_2D", "CEIL_2D", "ATT", "GEO"]

        try:
            with open(file_path, 'r') as file:
                self.content = file.read()

            # Check for required fields and validate DIMENSION
            for field in required_fields:
                field_value = self.get_field_value(field)
                if not field_value:
                    raise ValueError(f"Missing required field: {field}")
                if field == "DIMENSION" and (not field_value.isdigit() or int(field_value) <= 0):
                    raise ValueError(f"Invalid value for DIMENSION: {field_value}")

            # Validate EDGE_WEIGHT_TYPE
            self.edge_weight_type = self.get_field_value("EDGE_WEIGHT_TYPE")
            print(f"Set edge_weight_type to {self.edge_weight_type}")
            if self.edge_weight_type not in supported_types:
                raise ValueError(f"Unsupported EDGE_WEIGHT_TYPE: {self.edge_weight_type}")
            print(f"Finished validating file. edge_weight_type: {self.edge_weight_type}")

            # Fetch EDGE_WEIGHT_FORMAT if available
            self.edge_weight_format = self.get_field_value("EDGE_WEIGHT_FORMAT", optional=True)

            # Load city coordinates or distance matrix based on file type
            if self.edge_weight_type == "EXPLICIT":
                self._load_explicit_weights()
            elif "NODE_COORD_SECTION" in self.content:
                self._load_coordinates()

            print(f"File {os.path.basename(file_path)} passed validation.")

        except FileNotFoundError:
            print(f"File {file_path} not found.")
            raise
        except ValueError as ve:
            print(f"Validation error: {ve}")
            raise

    def _load_coordinates(self) -> None:
        """Load city coordinates from the NODE_COORD_SECTION."""
        self.coordinates = []
        in_node_coord_section = False
        for line in self.content.splitlines():
            if "NODE_COORD_SECTION" in line:
                in_node_coord_section = True
                continue
            if in_node_coord_section:
                if line.strip() == "EOF":
                    break
                parts = line.split()
                if len(parts) >= 3:
                    city_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                    self.coordinates.append((x, y))

    def load_display_coordinates(self) -> List[Tuple[float, float]]:
        """Load coordinates from the DISPLAY_DATA_SECTION if it exists."""
        display_coordinates = []
        in_display_section = False
        for line in self.content.splitlines():
            if "DISPLAY_DATA_SECTION" in line:
                in_display_section = True
                continue
            if in_display_section:
                if line.strip() == "EOF":
                    break
                parts = line.split()
                if len(parts) == 3:
                    node_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                    display_coordinates.append((x, y))
        return display_coordinates

    def generate_distance_matrix(self) -> None:
        """Generate a distance matrix based on EDGE_WEIGHT_TYPE."""
        print(f"Start generating distance matrix for {self.edge_weight_type}...")  # Dodaj log
        if self.edge_weight_type == "EUC_2D":
            self._calculate_euclidean_distance_2d()
            print("EUC_2D distance matrix generated.")
        elif self.edge_weight_type == "CEIL_2D":
            self._calculate_ceil_euclidean_distance_2d()
            print("CEIL_2D distance matrix generated.")
        elif self.edge_weight_type == "ATT":
            self._calculate_att_distance()
            print("ATT distance matrix generated.")
        elif self.edge_weight_type == "GEO":
            self._calculate_geographical_distance()
            print("GEO distance matrix generated.")
        elif self.edge_weight_type == "EXPLICIT":
            self._load_explicit_weights()
            print("Explicit distance matrix loaded.")
        else:
            raise ValueError(f"Unsupported EDGE_WEIGHT_TYPE: {self.edge_weight_type}")
        print(f"Finished generating distance matrix for {self.edge_weight_type}...")  # Dodaj log

    def _calculate_euclidean_distance_2d(self) -> None:
        """Calculate the Euclidean distance in 2D."""
        if not self.coordinates:
            raise ValueError("Coordinates are required for EUC_2D distance calculation.")

        num_cities = len(self.coordinates)
        self.distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                x1, y1 = self.coordinates[i]
                x2, y2 = self.coordinates[j]
                # Calculate the Euclidean distance and round it
                distance = int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + 0.5)
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance  # Symmetric matrix

        print(f"Distance matrix size: {len(self.distance_matrix)} x {len(self.distance_matrix[0])}")

        # Convert the entire matrix to integers
        self._convert_matrix_to_integers()

    def _calculate_ceil_euclidean_distance_2d(self) -> None:
        """Calculate the Euclidean distance in 2D and round it up."""
        if not self.coordinates:
            raise ValueError("Coordinates are required for CEIL_2D distance calculation.")

        num_cities = len(self.coordinates)
        self.distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]

        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                x1, y1 = self.coordinates[i]
                x2, y2 = self.coordinates[j]
                # Calculate the Euclidean distance
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                # Round the distance up
                ceil_distance = math.ceil(distance)
                self.distance_matrix[i][j] = ceil_distance
                self.distance_matrix[j][i] = ceil_distance  # Symmetric matrix

        # Convert the entire matrix to integers
        self._convert_matrix_to_integers()

    def _calculate_att_distance(self) -> None:
        """Calculate the pseudo-Euclidean ATT distance."""
        if not self.coordinates:
            raise ValueError("Coordinates are required for ATT distance calculation.")

        num_cities = len(self.coordinates)
        self.distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]

        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                x1, y1 = self.coordinates[i]
                x2, y2 = self.coordinates[j]

                # Calculate the differences in coordinates
                xd = x1 - x2
                yd = y1 - y2

                # Calculate the pseudo-Euclidean distance
                rij = math.sqrt((xd ** 2 + yd ** 2) / 10.0)
                tij = int(rij + 0.5)  # Round to the nearest integer

                # Check if tij is less than rij
                if tij < rij:
                    dij = tij + 1
                else:
                    dij = tij

                # Save the distance to the matrix
                self.distance_matrix[i][j] = dij
                self.distance_matrix[j][i] = dij  # Symmetric matrix

        # Convert the entire matrix to integers
        self._convert_matrix_to_integers()

    def _calculate_geographical_distance(self) -> None:
        """Calculate geographical distances."""
        if not self.coordinates:
            raise ValueError("Coordinates are required for GEO distance calculation.")

        PI = 3.141592
        RRR = 6378.388

        def to_radians(deg_min):
            """Convert coordinates from DDD.MM format to radians."""
            deg = int(deg_min)
            min = deg_min - deg
            return PI * (deg + 5.0 * min / 3.0) / 180.0

        num_cities = len(self.coordinates)
        self.distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]

        latitudes = []
        longitudes = []

        # Convert coordinates from DDD.MM format to radians
        for coord in self.coordinates:
            latitude, longitude = coord
            latitudes.append(to_radians(latitude))
            longitudes.append(to_radians(longitude))

        # Debugging print for converted coordinates in radians
        print("Converted coordinates in radians:")
        for i, (lat, lon) in enumerate(zip(latitudes, longitudes)):
            print(f"City {i + 1}: lat {lat}, lon {lon}")

        # Calculate the distances between cities
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                q1 = math.cos(longitudes[i] - longitudes[j])
                q2 = math.cos(latitudes[i] - latitudes[j])
                q3 = math.cos(latitudes[i] + latitudes[j])
                dij = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

                self.distance_matrix[i][j] = dij
                self.distance_matrix[j][i] = dij  # Symetryczna macierz

        print(f"Generated distance matrix for {len(self.distance_matrix)} cities)")

        # Convert the entire matrix to integers
        self._convert_matrix_to_integers()

        # Debug print for matrix size and sample rows
        print(f"Distance matrix size: {len(self.distance_matrix)} x {len(self.distance_matrix[0])}")
        print("Sample from distance matrix:")
        for row in self.distance_matrix[:5]:  # Print the first 5 rows as a sample
            print(row)

    def _load_explicit_weights(self) -> None:
        """Load explicit edge weights based on the format."""
        self.distance_matrix = []
        values = []

        # Fetch the DIMENSION value
        dimension = int(self.get_field_value("DIMENSION"))

        # Load values from the EDGE_WEIGHT_SECTION
        in_weight_section = False
        for line in self.content.splitlines():
            if any(section in line for section in ["DISPLAY_DATA_SECTION", "EOF", "NODE_COORD_SECTION"]):
                break
            if "EDGE_WEIGHT_SECTION" in line:
                in_weight_section = True
                continue
            if in_weight_section:
                values.extend(list(map(int, line.split())))

        # Map equivalent types
        if self.edge_weight_format == "LOWER_COL":
            self.edge_weight_format = "UPPER_ROW"
        elif self.edge_weight_format == "UPPER_COL":
            self.edge_weight_format = "LOWER_ROW"
        elif self.edge_weight_format == "LOWER_DIAG_COL":
            self.edge_weight_format = "UPPER_DIAG_ROW"
        elif self.edge_weight_format == "UPPER_DIAG_COL":
            self.edge_weight_format = "LOWER_DIAG_ROW"

        # Select the appropriate method based on format
        load_method = {
            "FULL_MATRIX": lambda: self._load_full_matrix(values, dimension),
            "LOWER_DIAG_ROW": lambda: self._load_triangular(values, dimension, lower=True, diag=True),
            "LOWER_ROW": lambda: self._load_triangular(values, dimension, lower=True, diag=False),
            "UPPER_DIAG_ROW": lambda: self._load_triangular(values, dimension, lower=False, diag=True),
            "UPPER_ROW": lambda: self._load_triangular(values, dimension, lower=False, diag=False),
        }

        load_method.get(self.edge_weight_format, self._unsupported_format)()

    def _load_full_matrix(self, values: List[int], dimension: int) -> None:
        """Load the full distance matrix."""
        self.distance_matrix = [values[i * dimension:(i + 1) * dimension] for i in range(dimension)]
        self._convert_matrix_to_integers()

    def _load_triangular(self, values: List[int], dimension: int, lower: bool, diag: bool) -> None:
        """
        Load a triangular matrix, with or without the diagonal.

        :param values: The distance values from the file.
        :param dimension: The number of cities (dimension of the matrix).
        :param lower: Whether the matrix is lower triangular.
        :param diag: Whether the diagonal is included.
        """
        self.distance_matrix = [[0] * dimension for _ in range(dimension)]
        value_index = 0

        for i in range(dimension):
            if lower:
                # If lower matrix, load below (or on) the diagonal
                for j in range(i + 1 if diag else i):
                    if value_index < len(values):
                        self.distance_matrix[i][j] = values[value_index]
                        self.distance_matrix[j][i] = values[value_index]  # Symetria
                        value_index += 1
            else:
                # If upper matrix, load above (or on) the diagonal
                for j in range(i if diag else i + 1, dimension):
                    if value_index < len(values):
                        self.distance_matrix[i][j] = values[value_index]
                        self.distance_matrix[j][i] = values[value_index]  # Symetria
                        value_index += 1

        # Convert the entire matrix to integers
        self._convert_matrix_to_integers()

    def _convert_matrix_to_integers(self) -> None:
        """Convert all values in the distance matrix to integers."""
        self.distance_matrix = [[int(value) for value in row] for row in self.distance_matrix]

    def _unsupported_format(self) -> None:
        """Handle unsupported formats."""
        raise ValueError(f"Unsupported EDGE_WEIGHT_FORMAT: {self.edge_weight_format}")

    def get_field_value(self, field_name: str, optional: bool = False) -> str or None:
        """
        Get the value of a specified field from the file content.

        :param field_name: The name of the field to retrieve.
        :param optional: Whether the field is optional.
        :return: The field value as a string or None if not found and optional is True.
        :raises ValueError: If the field is required and not found.
        """
        for line in self.content.splitlines():
            if line.startswith(field_name):
                return line.split(":")[1].strip()
        if not optional:
            raise ValueError(f"Field {field_name} not found in the file.")
        return None

    def get_distance_matrix(self) -> List[List[int]]:
        """
        Return the generated distance matrix.

        :return: The distance matrix as a 2D list of integers.
        """
        return self.distance_matrix
