cmake_minimum_required(VERSION 3.29)
project(tsp_optimization_application)

set(CMAKE_CXX_STANDARD 20)

# Znalezienie Pythona za pomocą nowego modułu FindPython
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Ustawienie, aby pybind11 używało nowego sposobu znajdowania Pythona
set(PYBIND11_FINDPYTHON ON)

# Znalezienie pybind11 zainstalowanego globalnie
find_package(pybind11 REQUIRED)

# Dodanie katalogu z plikami nagłówkowymi dla algorytmów SA i TS
include_directories(${CMAKE_SOURCE_DIR}/src/algorithms/cpp/SA)
include_directories(${CMAKE_SOURCE_DIR}/src/algorithms/cpp/TS)

# Dodanie modułu pybind11 dla plików cpp
pybind11_add_module(SimulatedAnnealing
        src/algorithms/cpp/SA/SimulatedAnnealing.cpp
        src/algorithms/cpp/bindings/SimulatedAnnealingBindings.cpp)

pybind11_add_module(TabuSearch
        src/algorithms/cpp/TS/TabuSearch.cpp
        src/algorithms/cpp/bindings/TabuSearchBindings.cpp)

# Ustawienie właściwości, aby wygenerować plik z prostą nazwą
set_target_properties(SimulatedAnnealing PROPERTIES PREFIX "" SUFFIX ".so" OUTPUT_NAME "SimulatedAnnealing")
set_target_properties(TabuSearch PROPERTIES PREFIX "" SUFFIX ".so" OUTPUT_NAME "TabuSearch")

# Ustawienie katalogu, do którego pliki .so będą zapisywane
set_target_properties(SimulatedAnnealing PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/compiled_binaries)
set_target_properties(TabuSearch PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/compiled_binaries)
