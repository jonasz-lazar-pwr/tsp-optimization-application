cmake_minimum_required(VERSION 3.29)
project(tsp_optimization_application)

set(CMAKE_CXX_STANDARD 20)

# Find Python using the new FindPython module
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Configure pybind11 to use the new way of finding Python
set(PYBIND11_FINDPYTHON ON)

# Find the globally installed pybind11 package
find_package(pybind11 REQUIRED)

# Find the NNG library
find_package(nng REQUIRED)

# Add include directories for NNG
include_directories(/opt/homebrew/opt/nng/include)

# Add library directories for NNG
link_directories(/opt/homebrew/opt/nng/lib)

# Add include directories for the SA and TS algorithm headers
include_directories(${CMAKE_SOURCE_DIR}/src/tsp_algorithms/sa)
include_directories(${CMAKE_SOURCE_DIR}/src/tsp_algorithms/sa/enums)
include_directories(${CMAKE_SOURCE_DIR}/src/tsp_algorithms/ts)
include_directories(${CMAKE_SOURCE_DIR}/src/tsp_algorithms/ts/TabuList)
include_directories(${CMAKE_SOURCE_DIR}/src/tsp_algorithms/ts/enums)
include_directories(${CMAKE_SOURCE_DIR}/src/tsp_algorithms/ts/utils)

# Add the pybind11 module for the Simulated Annealing files
pybind11_add_module(SimulatedAnnealing
        src/tsp_algorithms/sa/SimulatedAnnealing.cpp
        src/tsp_algorithms/bindings/SimulatedAnnealingBindings.cpp
        src/tsp_algorithms/sa/enums/InitialTempType.h
        src/tsp_algorithms/sa/enums/TempDecayType.h
        src/tsp_algorithms/sa/enums/MoveTypeSA.h
        src/tsp_algorithms/sa/enums/InitialSolutionTypeSA.h)

# Add the pybind11 module for the Tabu Search files
pybind11_add_module(TabuSearch
        src/tsp_algorithms/ts/TabuSearch.cpp
        src/tsp_algorithms/ts/TabuList/TabuList.cpp
        src/tsp_algorithms/ts/enums/MoveTypeTS.h
        src/tsp_algorithms/ts/enums/TenureType.h
        src/tsp_algorithms/ts/enums/TabuListLimitType.h
        src/tsp_algorithms/ts/enums/InitialSolutionTypeTS.h
        src/tsp_algorithms/ts/utils/MoveHashUtils.h
        src/tsp_algorithms/ts/utils/Neighbor.h
        src/tsp_algorithms/bindings/TabuSearchBindings.cpp)

# Link NNG to the target libraries
target_link_libraries(SimulatedAnnealing PRIVATE nng)
target_link_libraries(TabuSearch PRIVATE nng)

# Set properties to generate the file with a custom name
set_target_properties(SimulatedAnnealing PROPERTIES PREFIX "" SUFFIX ".so" OUTPUT_NAME "tsp_sa")
set_target_properties(TabuSearch PROPERTIES PREFIX "" SUFFIX ".so" OUTPUT_NAME "tsp_ts")

# Set the directory where the .so files will be saved
set_target_properties(SimulatedAnnealing PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/compiled_binaries)
set_target_properties(TabuSearch PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/compiled_binaries)
