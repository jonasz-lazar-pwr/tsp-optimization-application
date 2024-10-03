# src/tests/test_bulk_file_loader.py

import os
from src.backend.components.tsplib_management.tsplib_parser import TSPLIBParser

def validate_all_tsp_files(directory_path):
    """Validate all .tsp files in the given directory."""
    parser = TSPLIBParser()
    file_count = 0  # Inicjalizacja licznika

    # Iteruj przez wszystkie pliki w katalogu
    for file_name in os.listdir(directory_path):
        # Sprawdź, czy plik ma rozszerzenie .tsp
        if file_name.endswith(".tsp"):
            file_path = os.path.join(directory_path, file_name)
            print(f"Validating file: {file_name}")
            try:
                parser.validate_file(file_path)
                file_count += 1  # Zwiększenie licznika po udanej walidacji
            except ValueError as e:
                print(f"Validation failed for {file_name}: {e}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Wyświetl końcową liczbę przetworzonych plików
    print(f"\nTotal files validated: {file_count}")

if __name__ == "__main__":
    # Ścieżka do katalogu 'resources/tsplib', w którym znajdują się pliki .tsp
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../resources/tsplib')

    # Wywołaj funkcję, aby zwalidować wszystkie pliki .tsp w folderze
    validate_all_tsp_files(directory_path)