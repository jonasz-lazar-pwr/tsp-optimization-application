# Struktura projektu

```bash
tsp-optimization-application/
│
├── src/     
│   ├── main.py                            # Main application file
│   ├── config.py                          # Application configuration  
│   │       
│   ├── algorithms/                        # Directory for algorithm implementations
│   │   ├── python/                        # Algorithms in Python
│   │   └── cpp/                           # Algorithms in C++
│   │       ├── SA/                        # Simulated Annealing algorithm
│   │       │   ├── SimulatedAnnealing.cpp
│   │       │   └── SimulatedAnnealing.h
│   │       ├── TS/                        # Tabu Search algorithm
│   │       │   ├── TabuSearch.cpp
│   │       │   └── TabuSearch.h
│   │       └── bindings/                  # pybind11 bindings for C++ algorithms
│   │           ├── SimulatedAnnealingBindings.cpp
│   │           └── TabuSearchBindings.cpp
│   │
│   ├── backend/                           # Backend of the application
│   │   ├── components/                    # Backend components
│   │   │   ├── threads/                   # Threads for algorithms
│   │   │   │   └── algorithm_threads.py   # Algorithm threads management
│   │   │   └── tsplib_management/         # TSPLIB file management
│   │   │       ├── tsp_catalog.py         # Catalog management for TSPLIB files
│   │   │       ├── tsplib_parser.py       # TSPLIB file parser
│   │   │       └── tsp_file.py            # TSPLIB file handler
│   │   └── task_manager.py                # Task management
│   │
│   ├── gui/                               # GUI components
│   │   ├── components/                    # Separate files for each GUI component
│   │   │   └── directory_selector.py      # Directory selector for TSPLIB files
│   │   └── main_window.py                 # Main window of the application
│   │
│   └── utils/                             # Supporting utilities
│       └── interfaces/                    # Interfaces for classes
│
├── resources/                             # Project resources
│   ├── tsplib/                            # TSPLIB files for testing
│   ├── config/                            # Application configuration files
│   │   └── settings.json
│   ├── assets/                            # Icons, images, and text files
│   └── metadata/                          # Project metadata
│       └── optimal_results.json
│
├── tests/                                 # Test suite
│   ├── unit_tests/                        # Unit tests
│   └── integration_tests/                 # Integration tests
│
├── docs/                                  # Project documentation
│   └── project_structure.md               # Documentation of project structure
│
├── scripts/                               # Helper scripts for building, testing, etc.
│   └── build.py                           # Script for building the project
│
├── CMakeLists.txt                 # CMake build file for C++ components
├── requirements.txt               # List of Python dependencies (pip freeze)
├── LICENSE                        # Project license
├── .gitignore                     # Git ignore file
├── .gitattributes                 # Git attributes file
└── README.md                      # Project description
```
