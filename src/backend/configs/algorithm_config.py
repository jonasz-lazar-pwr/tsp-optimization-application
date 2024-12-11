# src/backend/configs/algorithm_config.py

from typing import Any


class AlgorithmConfig:
    def __init__(self, algorithms: list[str], file_name: str, sa_params: Any, sa_port: int,
                 ts_params: Any, ts_port: int, data_frequency: int):
        self.algorithms = algorithms
        self.file_name = file_name
        self.sa_params = sa_params
        self.sa_port = sa_port
        self.ts_params = ts_params
        self.ts_port = ts_port
        self.data_frequency = data_frequency
