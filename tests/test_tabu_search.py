# src/tests/test_tabu_search.py

import compiled_binaries.TabuSearch as TS
from src.backend.components.tsplib_management.tsp_file import TSPFile
from src.backend.components.tsplib_management.tsplib_parser import TSPLIBParser
from src.config import get_path

# Ścieżki do plików
tsp_file_path = get_path("resources/tsplib_test/berlin52.tsp")
optimal_results_path = get_path("resources/metadata/optimal_results.json")

# Inicjalizacja parsera TSPLIB
parser = TSPLIBParser()

# Inicjalizacja obiektu TSPFile, wczytanie pliku i macierzy odległości
tsp_file = TSPFile(file_path=tsp_file_path, optimal_results_path=optimal_results_path, parser=parser)
tsp_file.load_metadata()
tsp_file.load_distance_matrix()

# Pobranie macierzy odległości
distance_matrix = tsp_file.get_distance_matrix()

# Sprawdzenie, czy macierz odległości została poprawnie załadowana
if distance_matrix:


    # Stała kadencja
    # Losowa kadencja z zakresem
    ts_instance = TS.TabuSearch(tenure=100, dist_matrix=distance_matrix,
                                move_type=TS.MoveType.OPT_2, duration_ms=5000,
                                random_tenure_range=(50, 100), tenure_type=TS.TenureType.CONSTANT,
                                limit_type=TS.TabuListLimitType.CUSTOM, custom_limit=50, max_neighbors=100,
                                initial_solution_type=TS.InitialSolutionType.RANDOM)

    # Uruchomienie algorytmu TS
    ts_instance.run()

    # Wyświetlenie wyników
    print(f"Optimal Solution: {tsp_file.optimal_result}")
else:
    print("Failed to load distance matrix.")
