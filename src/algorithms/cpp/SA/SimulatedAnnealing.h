// src/algorithms/cpp/SA/SimulatedAnnealing.h

#ifndef SIMULATED_ANNEALING_H
#define SIMULATED_ANNEALING_H

#include <vector>
#include <string>

// Klasa reprezentująca algorytm Symulowanego Wyżarzania dla problemu TSP
class SimulatedAnnealing {
public:
    // Konstruktor przyjmujący końcową temperaturę, maksymalny czas wykonania, macierz odległości,
    // metody inicjalizacji temperatury, obniżania temperatury, sąsiada oraz parametry alfa i beta,
    // oraz liczbę kroków dla każdej temperatury
    SimulatedAnnealing(double final_temp, double duration,
                       const std::vector<std::vector<double>>& dist_matrix,
                       const std::string& temp_init_method, const std::string& temp_decay_method,
                       const std::string& neighbor_method, double alpha, double beta, int steps_per_temp);

    // Uruchamia algorytm i zwraca koszt najlepszej znalezionej trasy
    double run();

    // Getter for the current solution and its cost
    std::vector<int> get_current_solution() const;

    // Oblicza koszt (długość trasy) dla danego rozwiązania
    double calculate_cost(const std::vector<int>& solution) const;

private:
    // Metoda inicjalizująca początkowe losowe rozwiązanie
    void initialize_random_solution();

    // Metoda inicjalizująca temperaturę początkową na podstawie wybranej metody
    void initialize_temperature(const std::string& method);

    // Obniżenie temperatury na podstawie wybranej metody (geometric, logarithmic, linear)
    void apply_temperature_decay();

    // Generuje sąsiada obecnego rozwiązania na podstawie wybranej metody (swap, insert, invert)
    std::vector<int> generate_neighbor(const std::vector<int>& solution);

    // Metoda do inicjalizacji temperatury na podstawie średniej odległości
    double init_temp_avg_distance();

    // Metoda do inicjalizacji temperatury na podstawie maksymalnej odległości
    double init_temp_max_distance();

    // Metoda do inicjalizacji temperatury na podstawie losowej próbki różnic kosztów
    double init_temp_sampling();

    // Pomocnicza metoda do generowania losowej liczby całkowitej z zakresu [min, max]
    int generate_random_number(int min, int max);

    // Pomocnicza metoda do generowania losowej liczby zmiennoprzecinkowej w zakresie [0, 1)
    double generate_random_double();

    // Parametry algorytmu
    double temperature;               // Aktualna temperatura
    const double final_temperature;   // Końcowa temperatura
    const double max_duration;        // Maksymalny czas wykonania w sekundach
    const double alpha;               // Parametr dla obniżania geometrycznego
    const double beta;                // Parametr dla obniżania liniowego
    const int steps_per_temp;         // Liczba iteracji na daną temperaturę

    // Wybrana metoda inicjalizacji temperatury, metody obniżania temperatury i metody sąsiada
    const std::string temp_decay_method;
    const std::string neighbor_method;

    // Macierz odległości pomiędzy miastami
    const std::vector<std::vector<double>> distances;

    // Aktualne i najlepsze rozwiązanie oraz ich koszt
    std::vector<int> current_solution;
    double current_cost;
};

#endif // SIMULATED_ANNEALING_H
