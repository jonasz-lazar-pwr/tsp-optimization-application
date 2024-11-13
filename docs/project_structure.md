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
│   │   ├── configs/                            # Configuration files
│   │   ├── processes/                          # Processes for algorithm execution
│   │   ├── tsp_management/                     # TSPLIB file management
│   │   └── task_manager.py                     # Task management
│   │
│   ├── gui/                                    # GUI of the application
│   │   ├── dialogs/                            # Dialogs for the application
│   │   ├── panels/                             # Panels for the application
│   │   ├── widgets/                            # Widgets for the application
│   │   │   ├── management/                     # Widgets for management of settings and files
│   │   │   └── visualization/                  # Widgets for visualization of results
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
