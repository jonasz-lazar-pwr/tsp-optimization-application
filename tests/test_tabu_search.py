# src/tests/test_tabu_search.py

import multiprocessing
import time
import pynng

# Importy dla algorytmu TS i plików TSP
import compiled_binaries.TabuSearch as TS
from src.backend.components.tsp_management.tsp_file import TSPFile
from src.backend.components.tsp_management.tsplib_parser import TSPLIBParser
from src.utils.path_config import get_path

# Ścieżki do plików
tsp_file_path = get_path("data/tsplib/berlin52.tsp")
optimal_results_path = get_path("data/metadata/optimal_results.json")

# Inicjalizacja parsera TSPLIB
parser = TSPLIBParser()

# Inicjalizacja obiektu TSPFile, wczytanie pliku i macierzy odległości
tsp_file = TSPFile(file_path=tsp_file_path, optimal_results_path=optimal_results_path, parser=parser)
tsp_file.load_metadata()
tsp_file.load_distance_matrix()

# Pobranie macierzy odległości
distance_matrix = tsp_file.get_distance_matrix()

# Funkcja, która odbiera dane przez socket NNG
def receive_data():
    """Receives data from the TS process through the socket."""
    with pynng.Pair1() as sock:
        sock.listen('tcp://127.0.0.1:6666')  # Inny port dla TS
        while True:
            try:
                msg = sock.recv()
                message = msg.decode()
                if message == 'EOF':
                    print("Simulation finished.")
                    break
                print(f"Received message: {message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


# Funkcja, która uruchamia algorytm sa
def run_simulated_annealing():
    # Inicjalizacja algorytmu Tabu Search z parametrami
    ts_instance = TS.TabuSearch(
        tenure=100, dist_matrix=distance_matrix, move_type=TS.MoveType.OPT_2,
        duration_ms=3000, random_tenure_range=(50, 100), tenure_type=TS.TenureType.CONSTANT,
        limit_type=TS.TabuListLimitType.CUSTOM, custom_limit=50, max_neighbors=100,
        initial_solution_type=TS.InitialSolutionType.RANDOM
    )

    ts_instance.run()

    # Wyświetlenie wyników
    print("Optimal Solution:", tsp_file.optimal_result)


# Funkcja główna
if __name__ == '__main__':
    # Uruchomienie procesu dla odbierania danych
    ts_receiver_process = multiprocessing.Process(target=receive_data)
    ts_receiver_process.start()

    # Małe opóźnienie, aby upewnić się, że socket nasłuchuje
    time.sleep(1)

    # Uruchomienie procesu dla algorytmu sa
    ts_process = multiprocessing.Process(target=run_simulated_annealing)
    ts_process.start()

    # Oczekiwanie na zakończenie działania obu procesów
    ts_process.join()
    ts_process.join()
