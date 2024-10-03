# src/tests/test_file_loader.py

from src.backend.components.tsplib_management.tsplib_parser import TSPLIBParser


class ExtendedTSPLIBParser(TSPLIBParser):
    """Rozszerzona wersja parsera z możliwością wyświetlania macierzy odległości."""
    def validate_file(self, file_path):
        super().validate_file(file_path)
        self.display_distance_matrix()

    def display_distance_matrix(self):
        """Wyświetl fragment macierzy odległości."""
        matrix = self.get_distance_matrix()
        print("Distance Matrix:")
        for row in matrix:
            print(row)

if __name__ == "__main__":
    import sys
    import os
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Tworzenie instancji rozszerzonego parsera
    parser = ExtendedTSPLIBParser()

    # Ścieżka do katalogu 'resources/tsplib', w którym znajdują się pliki .tsp
    file_name = "upper_col.tsp"
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../resources/tsplib/example')
    file_path = os.path.join(directory_path, file_name)

    # Wyświetl absolutną ścieżkę do pliku, aby sprawdzić poprawność
    print(f"Absolutna ścieżka do pliku: {file_path}")

    # Sprawdzenie, czy plik istnieje
    if not os.path.isfile(file_path):
        print(f"Błąd: Plik {file_name} nie istnieje pod ścieżką {file_path}")
        sys.exit(1)

    # Wczytaj plik TSP
    parser.validate_file(file_path)

    # Wyświetl sumę odległości w kanonicznej trasie
    parser.get_canonical_tour_length()

    # Rozpocznij główną pętlę aplikacji
    sys.exit(app.exec())

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#
#     # Stwórz instancję rozszerzonego parsera
#     parser = ExtendedTSPLIBParser()
#
#     # Stwórz file loader z wstrzykniętym parserem
#     file_loader = FileLoader(parser)
#
#     # Wywołaj metodę załadowania pliku
#     file_loader.load_file()
#
#     # Rozpocznij główną pętlę aplikacji
#     sys.exit(app.exec())

    # def get_canonical_tour_length(self):
    #     """
    #     Oblicza i zwraca sumę odległości w kanonicznej trasie (miasta 0 -> 1 -> 2 -> ... -> n-1)
    #     :return: Całkowita długość trasy
    #     """
    #     if not self.distance_matrix:
    #         raise ValueError("Distance matrix is not initialized.")
    #
    #     num_cities = len(self.distance_matrix)
    #     total_length = 0
    #
    #     # Sumowanie dystansów pomiędzy miastami w kanonicznej trasie (0 -> 1 -> 2 -> ... -> n-1)
    #     for i in range(num_cities - 1):
    #         total_length += self.distance_matrix[i][i + 1]
    #
    #     # Dodaj dystans powrotny z ostatniego miasta do pierwszego
    #     total_length += self.distance_matrix[num_cities - 1][0]
    #
    #     print(f"Canonical tour length: {total_length}")
    #     return total_length