#include <string>
#include <vector>
#include <map>
#include <cmath>

#include "../lalib.hpp"  // Also includes ulib


/**
 * Compile at the main src directory with:
 * > g++ -std=c++17 -mavx -fopenmp -Wall lalib/tests/matrix_tests.cpp -lm -o matrix_tests.o
 * Run with:
 * > ./matrix_tests.o
 */


namespace internalMatrixTesting {

  using val_t = TEST_TYPE;
  using vect_t = decltype(ulib::choose_simd<val_t, true>());
  int vectSize = SIMD_SIZE / (int)sizeof(val_t);
  vect_t zeroVect = { };


  bool vectEq(vect_t vect1, vect_t vect2) {

    for (int vectElem = 0; vectElem < vectSize; vectElem++) {
      if ( vect1[vectElem] != vect2[vectElem] ) {
        return false;
      }
    }

    return true;
  }


  // Test 1
  bool test_zerosConstructor() {
    int correctRows = 9 + INDEX_OFFSET, correctCols = 11 + INDEX_OFFSET;

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>(correctRows, correctCols);

    int foundCols = testMatrix.numCols();
    int foundRows = testMatrix.numRows();

    bool passed = ((foundCols == correctCols) & (foundRows == correctRows));

    return passed;
  }


  // Test 2
  bool test_placeAndGet() {
    int correctCols = 11 + INDEX_OFFSET, correctRows = 9 + INDEX_OFFSET;

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>(correctRows, correctCols);

    val_t correctValue = 1.1;
    int col = 6, row = 3;
    testMatrix.place(row + INDEX_OFFSET, col + INDEX_OFFSET, correctValue);

    val_t foundValue = testMatrix(row + INDEX_OFFSET, col + INDEX_OFFSET);

    bool passed = (foundValue == correctValue);

    return passed;
  }


  // Test 3
  bool test_placeAndGetSIMD() {
    int correctRow = 3, correctVectIndex = 1;
    vect_t correctVect = zeroVect;
    correctVect[1] = 2.2;
    correctVect[2] = 3.3;

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>(correctRow + 1 + INDEX_OFFSET, (correctVectIndex + 1) * vectSize + INDEX_OFFSET);

    testMatrix.place(correctRow + INDEX_OFFSET, vectSize + 1 + INDEX_OFFSET, 2.2);
    testMatrix.place(correctRow + INDEX_OFFSET, vectSize + 2 + INDEX_OFFSET, 3.3);

    vect_t foundVect = testMatrix.getSIMD(correctRow + INDEX_OFFSET, correctVectIndex);

    bool passed = vectEq(foundVect, correctVect);

    return passed;
  }


  // Test 4
  bool test_arrayConstructor() {
    int nRows = 4 + INDEX_OFFSET, nCols = 8 + INDEX_OFFSET;
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>(nRows, nCols);

    correctMatrix.place(1 + INDEX_OFFSET, 1 + INDEX_OFFSET, 2.2);
    correctMatrix.place(2 + INDEX_OFFSET, 6 + INDEX_OFFSET, 3.3);

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>(nRows, nCols,
                                                           correctMatrix.getValues(),
                                                           correctMatrix.getColVectIndexes(),
                                                           correctMatrix.getRowPointers());

    bool passed = (testMatrix == correctMatrix);

    return passed;
  }


  // Test 5
  bool test_loadFromFileConstructor() {
    int nRows = 4 + INDEX_OFFSET, nCols = 8 + INDEX_OFFSET;
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>(nRows, nCols);

    correctMatrix.place(1 + INDEX_OFFSET, 1 + INDEX_OFFSET, 2.2);
    correctMatrix.place(2 + INDEX_OFFSET, 6 + INDEX_OFFSET, 3.3);

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix1.dat", 0);

    bool passed = (testMatrix == correctMatrix);

    return passed;
  }


  // Test 6
  bool test_elementWiseAddition() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2&3_add.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2 + matrix3;

    // Due to rounding the solutions might not be exact
    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 7
  bool test_elementWiseSubtraction() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2&3_sub.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2 - matrix3;

    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 8
  bool test_elementWiseMultiplication() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2&3_mul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2 * matrix3;

    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 9
  bool test_matrixVectorMultiplication() {
    lalib::Vector<val_t> correctVector = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/matrix2&vector1_matmul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
    lalib::Vector<val_t> vector1 = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/vector1.dat", 1);

    lalib::Vector<val_t> testVector = matrix2.matmul(vector1);

    bool passed = testVector.isClose(correctVector);

    return passed;
  }


  // Test 10
  bool test_rowDot() {
    lalib::Vector<val_t> correctVector = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/matrix2&vector1_matmul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
    lalib::Vector<val_t> vector1 = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/vector1.dat", 1);

    val_t testValue = matrix2.rowDot(2, vector1);

    bool passed = ( std::abs(testValue - correctVector(2)) < 1e-6 );

    return passed;
  }


  // Test 11
  bool test_naiveTranspose() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2_transpose.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.naiveTranspose();

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


  // Test 12
  bool test_transpose() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2_transpose.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.transpose();

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


    // Test 13
    bool test_transpose2() {
      lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2_transpose.dat", 1);
  
      lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
  
      lalib::Matrix<val_t> testMatrix = matrix2.transpose();
  
      bool passed = ( testMatrix.isClose(correctMatrix) );
  
      return passed;
    }


  // Test 14
  bool test_matrixMultiplication() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2&3_matmul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.matmul(matrix3);

    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 15
  bool test_frobenius() {
    val_t correctValue = 2.6376;  // Need to be updated from Matlab

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);

    val_t testValue = matrix2.frobenius();

    bool passed = ( std::abs(testValue - correctValue) < 1e-4 );

    return passed;
  }


  // Test 16
  bool test_save() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/matrix2.dat", 1);

    correctMatrix.save("tmp/matrix2_test.dat");

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>("tmp/matrix2_test.dat", INDEX_OFFSET);

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


  // Test 17
  bool test_largeElementWiseAddition() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2&3_add.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2 + matrix3;

    // Due to rounding the solutions might not be exact
    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 18
  bool test_largeElementWiseSubtraction() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2&3_sub.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2 - matrix3;

    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 19
  bool test_largeElementWiseMultiplication() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2&3_mul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2 * matrix3;

    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 20
  bool test_largeMatrixVectorMultiplication() {
    lalib::Vector<val_t> correctVector = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2&vector1_matmul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);
    lalib::Vector<val_t> vector1 = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/large_vector1.dat", 1);

    lalib::Vector<val_t> testVector = matrix2.matmul(vector1);

    bool passed = testVector.isClose(correctVector, (val_t)1e-5);

    return passed;
  }


  // Test 21
  bool test_largeRowDot() {
    lalib::Vector<val_t> correctVector = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2&vector1_matmul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);
    lalib::Vector<val_t> vector1 = lalib::Vector<val_t>("lalib/tests/test_files/matrix_tests/large_vector1.dat", 1);

    val_t testValue = matrix2.rowDot(2, vector1);

    bool passed = ( std::abs(testValue - correctVector(2)) < 1e-6 );

    return passed;
  }


  // Test 22
  bool test_largeNaiveTranspose() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2_transpose.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.naiveTranspose();

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


  // Test 23
  bool test_largeTranspose() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2_transpose.dat", 1);
    
    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.transpose();

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


  // Test 24
  bool test_largeTranspose2() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix4_transpose.dat", 1);
    
    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix4.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.transpose();

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


  // Test 25
  bool test_largeMatrixMultiplication() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2&3_matmul.dat", 1);

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);
    lalib::Matrix<val_t> matrix3 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix3.dat", 1);

    lalib::Matrix<val_t> testMatrix = matrix2.matmul(matrix3);

    bool passed = testMatrix.isClose(correctMatrix);

    return passed;
  }


  // Test 26
  bool test_largeFrobenius() {
    val_t correctValue = 215.1847;  // Need to be updated from Matlab

    lalib::Matrix<val_t> matrix2 = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);

    val_t testValue = matrix2.frobenius();

    bool passed = ( std::abs(testValue - correctValue) < 1e-4 );

    return passed;
  }


  // Test 27
  bool test_largeSave() {
    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>("lalib/tests/test_files/matrix_tests/large_matrix2.dat", 1);

    correctMatrix.save("tmp/large_matrix2_test.dat");

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>("tmp/large_matrix2_test.dat", INDEX_OFFSET);

    bool passed = ( testMatrix.isClose(correctMatrix) );

    return passed;
  }


  // Test 28
  bool test_identityConstructor() {
    int correctCols = 5 + INDEX_OFFSET, correctRows = 6 + INDEX_OFFSET;

    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>(correctRows, correctCols);

    val_t correctValue = 1.1;
    correctMatrix.place(0 + INDEX_OFFSET, 0 + INDEX_OFFSET, correctValue);
    correctMatrix.place(1 + INDEX_OFFSET, 1 + INDEX_OFFSET, correctValue);
    correctMatrix.place(2 + INDEX_OFFSET, 2 + INDEX_OFFSET, correctValue);
    correctMatrix.place(3 + INDEX_OFFSET, 3 + INDEX_OFFSET, correctValue);
    correctMatrix.place(4 + INDEX_OFFSET, 4 + INDEX_OFFSET, correctValue);

    lalib::Matrix<val_t> testMatrix = lalib::Matrix<val_t>(correctRows, correctCols, correctValue);

    bool passed = (correctMatrix == testMatrix);

    return passed;
  }


  // Test 29
  bool test_addRows() {
    int correctCols = 4 + INDEX_OFFSET, correctRows = 6 + INDEX_OFFSET;

    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>(correctRows, correctCols);

    val_t correctValue = 1.1;
    correctMatrix.place(0 + INDEX_OFFSET, 1 + INDEX_OFFSET, correctValue);
    correctMatrix.place(1 + INDEX_OFFSET, 1 + INDEX_OFFSET, correctValue);
    correctMatrix.place(2 + INDEX_OFFSET, 2 + INDEX_OFFSET, correctValue);
    correctMatrix.place(3 + INDEX_OFFSET, 3 + INDEX_OFFSET, correctValue);
    correctMatrix.place(2 + INDEX_OFFSET, 3 + INDEX_OFFSET, correctValue);
    correctMatrix.place(4 + INDEX_OFFSET, 2 + INDEX_OFFSET, correctValue);
    correctMatrix.place(5 + INDEX_OFFSET, 0 + INDEX_OFFSET, correctValue);

    lalib::Matrix<val_t> testMatrix1 = lalib::Matrix<val_t>(correctRows / 2, correctCols);
    lalib::Matrix<val_t> testMatrix2 = lalib::Matrix<val_t>(correctRows / 2, correctCols);

    testMatrix1.place(0 + INDEX_OFFSET, 1 + INDEX_OFFSET, correctValue);
    testMatrix1.place(1 + INDEX_OFFSET, 1 + INDEX_OFFSET, correctValue);
    testMatrix1.place(2 + INDEX_OFFSET, 2 + INDEX_OFFSET, correctValue);
    testMatrix1.place(2 + INDEX_OFFSET, 3 + INDEX_OFFSET, correctValue);
    testMatrix2.place(0 + INDEX_OFFSET, 3 + INDEX_OFFSET, correctValue);
    testMatrix2.place(1 + INDEX_OFFSET, 2 + INDEX_OFFSET, correctValue);
    testMatrix2.place(2 + INDEX_OFFSET, 0 + INDEX_OFFSET, correctValue);

    lalib::Matrix<val_t> foundMatrix = testMatrix1.addRows(testMatrix2);

    bool passed = (correctMatrix == foundMatrix);

    return passed;

  }


  // Test 30
  bool test_diagConstructor() {

    int correctCols = 4 + INDEX_OFFSET, correctRows = 4 + INDEX_OFFSET;

    lalib::Matrix<val_t> correctMatrix = lalib::Matrix<val_t>(correctRows, correctCols);

    correctMatrix.place(0 + INDEX_OFFSET, 0 + INDEX_OFFSET, 1.);
    correctMatrix.place(1 + INDEX_OFFSET, 1 + INDEX_OFFSET, 2.);
    correctMatrix.place(2 + INDEX_OFFSET, 2 + INDEX_OFFSET, 3.);
    correctMatrix.place(3 + INDEX_OFFSET, 3 + INDEX_OFFSET, 4.);

    lalib::Vector<val_t> diag = lalib::Vector<val_t>(correctRows);

    diag.place(0 + INDEX_OFFSET, 1.);
    diag.place(1 + INDEX_OFFSET, 2.);
    diag.place(2 + INDEX_OFFSET, 3.);
    diag.place(3 + INDEX_OFFSET, 4.);

    lalib::Matrix<val_t> foundMatrix = lalib::Matrix<val_t>(diag);

    bool passed = (correctMatrix == foundMatrix);

    return passed;

  }


  bool __addMatrixTests() {
    lalib::tests.addTest(test_zerosConstructor, "Matrix", "Zeros Constructor");
    lalib::tests.addTest(test_placeAndGet, "Matrix", "Place and Get");
    lalib::tests.addTest(test_placeAndGetSIMD, "Matrix", "Place and Get SIMD");
    lalib::tests.addTest(test_arrayConstructor, "Matrix", "Array Constructor");
    lalib::tests.addTest(test_loadFromFileConstructor, "Matrix", "File Constructor");
    lalib::tests.addTest(test_elementWiseAddition, "Matrix", "Elem Addition");
    lalib::tests.addTest(test_elementWiseSubtraction, "Matrix", "Elem Subtraction");
    lalib::tests.addTest(test_elementWiseMultiplication, "Matrix", "Elem Multiplication");
    lalib::tests.addTest(test_matrixVectorMultiplication, "Matrix", "Vector Matmul");
    lalib::tests.addTest(test_rowDot, "Matrix", "RowDot");
    lalib::tests.addTest(test_naiveTranspose, "Matrix", "Naive Transpose");
    lalib::tests.addTest(test_transpose, "Matrix", "Transpose");
    lalib::tests.addTest(test_transpose2, "Matrix", "Non-square Transpose");
    lalib::tests.addTest(test_matrixMultiplication, "Matrix", "Matmul");
    lalib::tests.addTest(test_frobenius, "Matrix", "Frobenius");
    lalib::tests.addTest(test_save, "Matrix", "Save");
    lalib::tests.addTest(test_largeElementWiseAddition, "Matrix", "Large Elem Addition");
    lalib::tests.addTest(test_largeElementWiseSubtraction, "Matrix", "Large Elem Subtraction");
    lalib::tests.addTest(test_largeElementWiseMultiplication, "Matrix", "Large Elem Multiplication");
    lalib::tests.addTest(test_largeMatrixVectorMultiplication, "Matrix", "Large Vector Matmul");
    lalib::tests.addTest(test_largeRowDot, "Matrix", "Large RowDot");
    lalib::tests.addTest(test_largeNaiveTranspose, "Matrix", "Large Naive Transpose");
    lalib::tests.addTest(test_largeTranspose, "Matrix", "Large Transpose");
    lalib::tests.addTest(test_largeTranspose2, "Matrix", "Large Non-square Transpose");
    lalib::tests.addTest(test_largeMatrixMultiplication, "Matrix", "Large Matmul");
    lalib::tests.addTest(test_largeFrobenius, "Matrix", "Large Frobenius");
    lalib::tests.addTest(test_largeSave, "Matrix", "Large Save");
    lalib::tests.addTest(test_identityConstructor, "Matrix", "Identity constructor");
    lalib::tests.addTest(test_addRows, "Matrix", "Adding rows");
    lalib::tests.addTest(test_diagConstructor, "Matrix", "Diagonal constructor");
    return true;
  }

  bool matrixTestsAddedToTestSuite = __addMatrixTests();

}

/*
int main() {
  ulib::verbosity(5);
  lalib::tests.runTests();
}
*/
