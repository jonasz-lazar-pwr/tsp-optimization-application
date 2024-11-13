# src/backend/components/ts_parameters.py

from enum import Enum
import compiled_binaries.tsp_ts as ts


class NeighborSelectionMethodTS(Enum):
    SWAP = "SWAP"
    OPT_2 = "OPT_2"

class TabuListLimitMethodTS(Enum):
    N = "N"
    SQRT_N = "SQRT_N"
    THREE_N = "THREE_N"
    N_SQUARED = "N_SQUARED"
    CUSTOM = "CUSTOM"

class InitialSolutionMethodTS(Enum):
    RANDOM = "RANDOM"
    GREEDY = "GREEDY"

class TenureTypeTS(Enum):
    CONSTANT = "CONSTANT"
    RANDOM = "RANDOM"

def map_neighbor_selection_method(method: NeighborSelectionMethodTS) -> ts.NeighborSelectionMethodTS:
    """
    Maps the NeighborSelectionMethodTS enum to the corresponding C++ enum.

    :param method: An instance of NeighborSelectionMethodTS.
    :return: The corresponding ts.NeighborSelectionMethodTS enum value.
    :raises ValueError: If the method is unknown.
    """
    if method == NeighborSelectionMethodTS.SWAP:
        return ts.NeighborSelectionMethodTS.SWAP
    elif method == NeighborSelectionMethodTS.OPT_2:
        return ts.NeighborSelectionMethodTS.OPT_2
    else:
        raise ValueError(f"Unknown MoveTypeTS: {method}")

def map_tabu_list_limit_method(method: TabuListLimitMethodTS) -> ts.TabuListLimitMethodTS:
    """
    Maps the TabuListLimitMethodTS enum to the corresponding C++ enum.

    :param method: An instance of TabuListLimitMethodTS.
    :return: The corresponding ts.TabuListLimitMethodTS enum value.
    :raises ValueError: If the method is unknown.
    """
    if method == TabuListLimitMethodTS.N:
        return ts.TabuListLimitMethodTS.N
    elif method == TabuListLimitMethodTS.SQRT_N:
        return ts.TabuListLimitMethodTS.SQRT_N
    elif method == TabuListLimitMethodTS.THREE_N:
        return ts.TabuListLimitMethodTS.THREE_N
    elif method == TabuListLimitMethodTS.N_SQUARED:
        return ts.TabuListLimitMethodTS.N_SQUARED
    elif method == TabuListLimitMethodTS.CUSTOM:
        return ts.TabuListLimitMethodTS.CUSTOM
    else:
        raise ValueError(f"Unknown TabuListLimitType: {method}")

def map_initial_solution_method(method: InitialSolutionMethodTS) -> ts.InitialSolutionMethodTS:
    """
    Maps the InitialSolutionMethodTS enum to the corresponding C++ enum.

    :param method: An instance of InitialSolutionMethodTS.
    :return: The corresponding ts.InitialSolutionMethodTS enum value.
    :raises ValueError: If the method is unknown.
    """
    if method == InitialSolutionMethodTS.RANDOM:
        return ts.InitialSolutionMethodTS.RANDOM
    elif method == InitialSolutionMethodTS.GREEDY:
        return ts.InitialSolutionMethodTS.GREEDY
    else:
        raise ValueError(f"Unknown InitialSolutionTypeTS: {method}")

def map_tenure_type(method: TenureTypeTS) -> ts.TenureTypeTS:
    """
    Maps the TenureTypeTS enum to the corresponding C++ enum.

    :param method: An instance of TenureTypeTS.
    :return: The corresponding ts.TenureTypeTS enum value.
    :raises ValueError: If the method is unknown.
    """
    if method == TenureTypeTS.CONSTANT:
        return ts.TenureTypeTS.CONSTANT
    elif method == TenureTypeTS.RANDOM:
        return ts.TenureTypeTS.RANDOM
    else:
        raise ValueError(f"Unknown TenureType: {method}")

class TSParameters:
    def __init__(self, duration_ms: int, tenure_type: TenureTypeTS, constant_tenure: int,
                 random_tenure_range: tuple[int, int], tabu_list_limit_method: TabuListLimitMethodTS,
                 tabu_list_custom_limit: int, max_neighbors: int, neighbor_selection_method: NeighborSelectionMethodTS,
                 initial_solution_method: InitialSolutionMethodTS) -> None:
        """
        Initializes the parameters for the Tabu Search algorithm.

        :param duration_ms: Maximum duration of the algorithm in milliseconds.
        :param tenure_type: Type of tenure for the tabu list.
        :param constant_tenure: Constant tenure if tenure_type is CONSTANT.
        :param random_tenure_range: Range for tenure if tenure_type is RANDOM.
        :param tabu_list_limit_method: Method for limiting the size of the tabu list.
        :param tabu_list_custom_limit: Custom limit for the tabu list size.
        :param max_neighbors: Maximum number of neighbors to explore.
        :param neighbor_selection_method: Method for neighbor selection.
        :param initial_solution_method: Method for generating the initial solution.
        :return: None
        """
        self.duration_ms: int = duration_ms
        self.tenure_type: TenureTypeTS = tenure_type
        self.constant_tenure: int = constant_tenure
        self.random_tenure_range: tuple[int, int] = random_tenure_range
        self.tabu_list_limit_method: TabuListLimitMethodTS = tabu_list_limit_method
        self.tabu_list_custom_limit: int = tabu_list_custom_limit
        self.max_neighbors: int = max_neighbors
        self.neighbor_selection_method: NeighborSelectionMethodTS = neighbor_selection_method
        self.initial_solution_method: InitialSolutionMethodTS = initial_solution_method

    def to_dict(self) -> dict:
        """
        Converts the TS parameters to a dictionary format.

        :return: A dictionary representation of the parameters.
        """
        return {
            "duration_ms": self.duration_ms,
            "initial_solution_method": self.initial_solution_method.value,
            "neighbor_selection_method": self.neighbor_selection_method.value,
            "max_neighbors": self.max_neighbors,
            "tabu_list_limit_method": self.tabu_list_limit_method.value,
            "tabu_list_custom_limit": self.tabu_list_custom_limit,
            "tenure_type": self.tenure_type.value,
            "constant_tenure": self.constant_tenure,
            "random_tenure_range": self.random_tenure_range,
        }
