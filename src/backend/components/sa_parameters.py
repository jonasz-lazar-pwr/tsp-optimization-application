# src/backend/components/sa_parameters.py

from enum import Enum
import compiled_binaries.tsp_sa as sa


class InitialTempMethodSA(Enum):
    AVG = "AVG"
    MAX = "MAX"
    SAMPLING = "SAMPLING"

class NeighborSelectionMethodSA(Enum):
    SWAP = "SWAP"
    INSERT = "INSERT"
    INVERT = "INVERT"

class InitialSolutionMethodSA(Enum):
    RANDOM = "RANDOM"
    GREEDY = "GREEDY"


def map_initial_temp_method(method: InitialTempMethodSA) -> sa.InitialTempMethodSA:
    """
    Maps the InitialTempMethodSA enumeration to the corresponding C++ enum.

    :param method: An InitialTempMethodSA enum instance.
    :return: The corresponding sa.InitialTempMethodSA enum value.
    :raises ValueError: If an unknown method is provided.
    """
    if method == InitialTempMethodSA.AVG:
        return sa.InitialTempMethodSA.AVG
    elif method == InitialTempMethodSA.MAX:
        return sa.InitialTempMethodSA.MAX
    elif method == InitialTempMethodSA.SAMPLING:
        return sa.InitialTempMethodSA.SAMPLING
    else:
        raise ValueError(f"Unknown InitialTempMethodSA: {method}")


def map_neighbor_selection_method(method: NeighborSelectionMethodSA) -> sa.NeighborSelectionMethodSA:
    """
    Maps the NeighborSelectionMethodSA enumeration to the corresponding C++ enum.

    :param method: A NeighborSelectionMethodSA enum instance.
    :return: The corresponding sa.NeighborSelectionMethodSA enum value.
    :raises ValueError: If an unknown method is provided.
    """
    if method == NeighborSelectionMethodSA.SWAP:
        return sa.NeighborSelectionMethodSA.SWAP
    elif method == NeighborSelectionMethodSA.INSERT:
        return sa.NeighborSelectionMethodSA.INSERT
    elif method == NeighborSelectionMethodSA.INVERT:
        return sa.NeighborSelectionMethodSA.INVERT
    else:
        raise ValueError(f"Unknown NeighborSelectionMethodSA: {method}")

def map_initial_solution_method(method: InitialSolutionMethodSA) -> sa.InitialSolutionMethodSA:
    """
    Maps the InitialSolutionMethodSA enumeration to the corresponding C++ enum.

    :param method: An InitialSolutionMethodSA enum instance.
    :return: The corresponding sa.InitialSolutionMethodSA enum value.
    :raises ValueError: If an unknown method is provided.
    """
    if method == InitialSolutionMethodSA.RANDOM:
        return sa.InitialSolutionMethodSA.RANDOM
    elif method == InitialSolutionMethodSA.GREEDY:
        return sa.InitialSolutionMethodSA.GREEDY
    else:
        raise ValueError(f"Unknown InitialSolutionMethodSA: {method}")

class SAParameters:
    def __init__(self, duration_ms: int, initial_temp_method: InitialTempMethodSA,
                 alpha: float, steps_per_temp: int, neighbor_selection_method: NeighborSelectionMethodSA,
                 initial_solution_method: InitialSolutionMethodSA) -> None:
        """
        Initializes the parameters for the Simulated Annealing algorithm.

        :param duration_ms: The maximum algorithm duration in milliseconds.
        :param initial_temp_method: Method for calculating initial temperature.
        :param alpha: Cooling factor.
        :param steps_per_temp: Number of iterations at each temperature level.
        :param neighbor_selection_method: Method for neighbor selection.
        :param initial_solution_method: Method for generating the initial solution.
        :return: None
        """
        self.duration_ms: int = duration_ms
        self.initial_temp_method: InitialTempMethodSA = initial_temp_method
        self.alpha: float = alpha
        self.steps_per_temp: int = steps_per_temp
        self.neighbor_selection_method: NeighborSelectionMethodSA = neighbor_selection_method
        self.initial_solution_method: InitialSolutionMethodSA = initial_solution_method

    def to_dict(self) -> dict:
        """
        Converts the SA parameters into a dictionary format.

        :return: A dictionary representation of the parameters.
        """
        return {
            "duration_ms": self.duration_ms,
            "initial_temp_method": self.initial_temp_method.value,
            "initial_solution_method": self.initial_solution_method.value,
            "neighbor_selection_method": self.neighbor_selection_method.value,
            "steps_per_temp": self.steps_per_temp,
            "alpha": self.alpha,
        }
