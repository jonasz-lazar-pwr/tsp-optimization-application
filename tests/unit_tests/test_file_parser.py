# src/tests/test_file_parser.py
from src.backend.components.tsplib_management.tsplib_parser import TSPLIBParser


def test_euclidean_distance():
    parser = TSPLIBParser()
    parser.validate_file("path/to/berlin52.tsp")

    # Pobranie macierzy odległości
    distance_matrix = parser.get_distance_matrix()

    # Wyświetlenie fragmentu macierzy
    for row in distance_matrix[:5]:
        print(row)

if __name__ == "__main__":
    test_euclidean_distance()