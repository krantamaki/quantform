#include <string>
#include <vector>
#include <map>
#include <cmath>

#include "../lalib.hpp"  // Also includes ulib


/**
 * Compile at the main src directory with:
 * > g++ -std=c++17 -mavx -fopenmp -Wall lalib/tests/solver_tests.cpp -lm -o solver_tests.o
 * Run with:
 * > ./solver_tests.o
 *
 * Note that the test matrices used here are purely randomly selected s.p.d matrices 
 * so the non-zero values are very unevenly distributed, which leads to lesser efficiency 
 * when using SIMD commands
 */


namespace internalLinearSolverTesting {

  using val_t = TEST_TYPE;
  using vect_t = decltype(ulib::choose_simd<val_t, true>());
  int vectSize = SIMD_SIZE / (int)sizeof(val_t);
  vect_t zeroVect = { };


  bool test_cg_small() {

    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_small.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_small.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CG", x0);
    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cgnr_small() {

    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_small.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_small.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CGNR", x0);
    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cg_medium() {

    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_medium.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_medium.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CG", x0);
    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cgnr_medium() {

    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_medium.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_medium.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CGNR", x0);
    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cg_large() {

    // Solving in Matlab using the backslash operator took around 50ms
    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_large.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_large.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CG", x0);

    LOWPRIORITY(ulib::formString("Time taken: ", solver.getSolveTime(), " ms"));

    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cgnr_large() {

    // Solving in Matlab using the backslash operator took around 50ms
    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_large.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_large.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CGNR", x0);

    LOWPRIORITY(ulib::formString("Time taken: ", solver.getSolveTime(), " ms"));

    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cg_huge() {

    // Solving in Matlab using the backslash operator took around 300ms
    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_huge.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_huge.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CG", x0);

    LOWPRIORITY(ulib::formString("Time taken: ", solver.getSolveTime(), " ms"));

    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cgnr_huge() {

    // Solving in Matlab using the backslash operator took around 300ms
    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_huge.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_huge.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CGNR", x0);

    LOWPRIORITY(ulib::formString("Time taken: ", solver.getSolveTime(), " ms"));

    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cg_massive() {

    // Solving in Matlab using the backslash operator took around 450ms
    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_massive.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_massive.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CG", x0);

    LOWPRIORITY(ulib::formString("Time taken: ", solver.getSolveTime(), " ms"));

    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool test_cgnr_massive() {

    // Solving in Matlab using the backslash operator took around 450ms
    lalib::Matrix<val_t> A = lalib::Matrix<val_t>("lalib/tests/test_files/solver_tests/linsys_A_massive.dat", 1);
    lalib::Vector<val_t> b = lalib::Vector<val_t>("lalib/tests/test_files/solver_tests/linsys_b_massive.dat", 1);

    lalib::Vector<val_t> x0 = lalib::Vector<val_t>(b.len());
    lalib::LinearSolver<val_t> solver = lalib::LinearSolver<val_t>(A, b);

    solver.solve("CGNR", x0);

    LOWPRIORITY(ulib::formString("Time taken: ", solver.getSolveTime(), " ms"));

    lalib::Vector<val_t> x = solver.getSolution();
    lalib::Vector<val_t> b_tmp = A.matmul(x);

    bool passed = b.isClose(b_tmp, 1e-2);

    return passed;
  }


  bool __addLinearSolverTests() {
    lalib::tests.addTest(test_cg_small);
    lalib::tests.addTest(test_cgnr_small);
    lalib::tests.addTest(test_cg_medium);
    lalib::tests.addTest(test_cgnr_medium);
    lalib::tests.addTest(test_cg_large);
    lalib::tests.addTest(test_cgnr_large);
    lalib::tests.addTest(test_cg_huge);
    lalib::tests.addTest(test_cgnr_huge);
    lalib::tests.addTest(test_cg_massive);
    lalib::tests.addTest(test_cgnr_massive);
    
    return true;
  }

  bool linearSolverTestsAddedToTestSuite = __addLinearSolverTests();
}

/*
int main() {
  ulib::verbosity(5);
  lalib::tests.runTests();
}
*/
