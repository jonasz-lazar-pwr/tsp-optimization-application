# Project structure

```bash
tsp-optimization-application/
│
├── src/     
│   ├── main.py                                 # Main application file
│   │       
│   ├── tsp_algorithms/                         # SA and TS algorithms in C++
│   │   ├── bindings/                           # pybind11 bindings for C++ algorithms
│   │   │   ├── SimulatedAnnealingBindings.cpp  # pybind11 bindings for SA
│   │   │   └── TabuSearchBindings.cpp          # pybind11 bindings for TS
│   │   │
│   │   ├── sa/                                 # Simulated Annealing algorithm
│   │   │   ├── enums/                          # Enumerations for SA
│   │   │   ├── SimulatedAnnealing.cpp          # C++ implementation of SA
│   │   │   └── SimulatedAnnealing.h            # Header file for SA
│   │   │
│   │   └── ts/                                 # Tabu Search algorithm
│   │       ├── enums/                          # Enumerations for TS
│   │       ├── TabuSearch.cpp                  # C++ implementation of TS
│   │       └── TabuSearch.h                    # Header file for TS
│   │
│   ├── backend/                                # Backend of the application
│   │   ├── components/                         # Backend components
│   │   │   ├── processes/                      # Processes for algorithm execution
│   │   │   └── tsp_management/                 # TSPLIB file management
│   │   └── task_manager.py                     # Task management
│   │
│   ├── gui/                                    # GUI of the application
│   │   ├── components/                         # GUI components
│   │   │   └── plots/                          # Plotting components
│   │   └── main_window.py                      # Main window of the application
│   │
│   └── utils/                                  # Supporting utilities
│       └── path_config.py                      # Path configuration
│
├── data/                                       # Project data
│   ├── tsplib/                                 # TSPLIB files for testing
│   ├── config/                                 # Application configuration files
│   │   └── settings.json
│   ├── assets/                                 # Icons, images, and text files
│   └── metadata/                               # Project metadata
│       └── optimal_results.json
│
├── tests/                                      # Test suite
│
├── docs/                                       # Project documentation
│   └── project_structure.md                    # Documentation of project structure
│
├── CMakeLists.txt                              # CMake build file for C++ components
├── requirements.txt                            # List of Python dependencies (pip freeze)
├── LICENSE                                     # Project license
├── .gitignore                                  # Git ignore file
├── .gitattributes                              # Git attributes file
└── README.md                                   # Project description
```
