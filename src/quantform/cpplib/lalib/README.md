## Linear Algebra Library

A general purpose linear algebra library with a multithreaded and vectorized implementation for sparse matrices. Used as subprocesses by the _cfopt_ software.

Implemented in C++

### Description of each file

- _src/Matrix.hpp_ : Contains the implementation of the _Matrix_ class template. This is the sparse and vectorized matrix used in the code.
- _src/Vector.hpp_ : Contains the implementation of the _Vector_ class template. This is also vectorized, but not sparse as that would be unnecessary in practice.
- _src/LinearSolver.hpp_ : Contains the implementation of the _LinearSolver_ class template, that mainly just contains the _solve_ method that solves the given problem with the wanted method.
- _lalib.hpp_ : The file that one should include to access the library.