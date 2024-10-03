# src/backend/components/threads/algorithm_threads.py

from PySide6.QtCore import QThread, Signal

# Thread class for Simulated Annealing
class SimulatedAnnealingThread(QThread):
    result_signal = Signal(float)         # Emit final cost
    solution_signal = Signal(list)        # Emit current solution after each iteration

    def __init__(self, sa_instance):
        super().__init__()
        self.sa_instance = sa_instance

    def run(self):
        print("Running Simulated Annealing algorithm...")
        try:
            max_iterations = self.sa_instance.get_max_iterations()

            # Ostatnia iteracja będzie zawierać ostateczne rozwiązanie
            final_solution = None

            for i in range(max_iterations):
                # Execute one iteration and get the current solution
                current_solution = self.sa_instance.iterate()
                print(f"Iteration {i}: Received solution {current_solution}")  # Logowanie

                # Emit the current solution in each iteration
                self.solution_signal.emit(current_solution)

                # Save the final solution
                final_solution = current_solution

            # Po zakończeniu iteracji zwracamy ostateczne rozwiązanie
            print(f"Algorithm finished with final solution: {final_solution}")
            final_cost = self.sa_instance.calculate_cost(final_solution)  # Obliczamy ostateczny koszt
            self.result_signal.emit(final_cost)  # Emit the final cost

        except Exception as e:
            print(f"Error during algorithm execution: {e}")

# # src/gui/components/threads/algorithm_threads.py
#
# from PySide6.QtCore import QThread, Signal
#
# # Thread class for Simulated Annealing
# class SimulatedAnnealingThread(QThread):
#     result_signal = Signal(float)         # Emit final cost
#     solution_signal = Signal(list)        # Emit current solution after each iteration
#
#     def __init__(self, sa_instance):
#         super().__init__()
#         self.sa_instance = sa_instance
#
#     def run(self):
#         print("Running Simulated Annealing algorithm...")
#         try:
#             # Zamiast bezpośrednio używać sa_instance.max_iterations, użyjemy metody
#             max_iterations = self.sa_instance.get_max_iterations()
#
#             for i in range(max_iterations):
#                 # Execute one iteration and get the current solution
#                 current_solution = self.sa_instance.iterate()
#                 print(f"Iteration {i}: Received solution {current_solution}")  # Logowanie
#                 # Emit the current solution in each iteration
#                 self.solution_signal.emit(current_solution)
#
#             # Po zakończeniu iteracji, oblicz i zwróć ostateczny koszt
#             final_result = self.sa_instance.run()
#             print(f"Algorithm finished with result: {final_result}")
#             self.result_signal.emit(final_result)
#         except Exception as e:
#             print(f"Error during algorithm execution: {e}")

# # src/gui/components/threads/algorithm_threads.py
#
# from PySide6.QtCore import QThread, Signal
#
# # Thread class for Simulated Annealing
# class SimulatedAnnealingThread(QThread):
#     result_signal = Signal(int)
#
#     def __init__(self, sa_instance):
#         super().__init__()
#         self.sa_instance = sa_instance
#
#     def run(self):
#         print("Running Simulated Annealing algorithm...")  # Log start
#         try:
#             # Execute the algorithm
#             result = self.sa_instance.run()
#             print(f"Algorithm finished with result: {result}")  # Log result
#             # Emit the result through the signal
#             self.result_signal.emit(result)
#         except Exception as e:
#             print(f"Error during algorithm execution: {e}")  # Log any exceptions
