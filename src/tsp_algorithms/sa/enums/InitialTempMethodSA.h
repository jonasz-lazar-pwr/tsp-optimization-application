// src/tsp_algorithms/sa/enums/InitialTempMethodSA.h

#ifndef INITIALTEMPMETHODSA_H
#define INITIALTEMPMETHODSA_H


// Enum defining the method for generating the initial temperature
enum class InitialTempMethodSA {
  AVG, // Average distance-based initial temperature
  MAX, // Maximum distance-based initial temperature
  SAMPLING // Sampling-based initial temperature (using random cost differences)
};

#endif //INITIALTEMPMETHODSA_H
