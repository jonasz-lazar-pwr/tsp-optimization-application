import multiprocessing
import time
import pynng

# Importy dla algorytmu sa i plików TSP
import compiled_binaries.SimulatedAnnealing as SA
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
    with pynng.Pair1() as sock:
        sock.listen('tcp://127.0.0.1:5555')  # Ustawienie socketu w trybie nasłuchiwania
        print("Waiting for connection...")
        while True:
            try:
                msg = sock.recv()  # Blokuje i czeka na wiadomość
                message = msg.decode()
                print(f"Received message: {message}")
                if message == 'EOF':
                    print("Simulation finished.")
                    break

                # # Wyślij potwierdzenie (ACK)
                # ack_message = "ACK " + message.split(" ")[0]
                # sock.send(ack_message.encode())

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

# Funkcja, która uruchamia algorytm sa
def run_simulated_annealing():
    # Inicjalizacja algorytmu sa
    sa_instance = SA.SimulatedAnnealing(final_temp=1e-4, duration_ms=15000, dist_matrix=distance_matrix,
                                        initial_temp_type=SA.InitialTempType.SAMPLING, temp_decay_type=SA.TempDecayType.GEO,
                                        move_type=SA.MoveType.INSERT, alpha=0.99, beta=0.1, steps_per_temp=2000,
                                        initial_solution_type=SA.InitialSolutionType.RANDOM)

    # Uruchomienie algorytmu
    sa_instance.run()

    # Wyświetlenie wyników
    print("Optimal Solution:", tsp_file.optimal_result)

# Funkcja główna
if __name__ == '__main__':
    # Uruchomienie procesu dla odbierania danych
    receiver_process = multiprocessing.Process(target=receive_data)
    receiver_process.start()

    # Małe opóźnienie, aby upewnić się, że socket nasłuchuje
    time.sleep(2)

    # Uruchomienie procesu dla algorytmu sa
    sa_process = multiprocessing.Process(target=run_simulated_annealing)
    sa_process.start()

    # Oczekiwanie na zakończenie działania obu procesów
    sa_process.join()
    receiver_process.join()
